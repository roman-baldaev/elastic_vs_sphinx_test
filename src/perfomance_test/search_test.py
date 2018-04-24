from abc import abstractmethod, ABC
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from time import clock
from pandas import read_csv
from pandas import DataFrame
from pandas import concat


class SearchTest(ABC):
    """
    An abstract class that defines the basic interface for search tests in various objects(Elastic, MongoDB).
    'file_for_save' - path to CSV-file for save tests results
    'time' - time of executing search query
    'size' - size of test object
    'query' - search query in human readable form
    'total' - total number of documents found
    """
    def __init__(self, file_for_save, object_test_name=None):
        self.object_test_name = object_test_name
        self.file_for_save = file_for_save
        self.time = None
        self.results = None
        self.size = None
        self.query = None
        self.total = None

    def __save__(self):
        """
        This method is called by the search functions ('search_substring' etc) after the
        search is completed to save the test results.
        """

        _columns = ['index', 'size', 'query', 'time', 'total']
        data = [self.object_test_name, self.size, self.query, self.time, self.total]

        source = read_csv(self.file_for_save)
        # save data of search test in DataFrame format and
        dataframe_for_save = DataFrame([data], columns=_columns)
        _sum = concat([source, dataframe_for_save], ignore_index=True)

        _sum.to_csv(self.file_for_save, index=False)

    @property
    @classmethod
    def test_name(cls):
        return cls.__name__

    @abstractmethod
    def search_substring(self, substrings, field):
        ...

    @abstractmethod
    def size_of_object(self):
        ...


class SearchTestElastic(SearchTest):
    """
    'object_test_name' for Elasticsearch its name of index
    'timeout' - A search timeout, bounding the search request to be executed within
                the specified time value and bail with the hits accumulated up to that point when expired.
    """
    def __init__(self, timeout=10, *args, **kwargs):
        super(SearchTestElastic, self).__init__(*args, **kwargs)
        self.client = Elasticsearch(timeout)

    def search_substring(self, substrings, _index):
        """
        Search all 'substrings' in 'index' ES
        :param substrings: substrings list
        :param _index: ES index
        """

        self.size = self.size_of_object(_index)
        self.object_test_name = _index

        # each substring search is stored as a result of a separate test.
        for substring in substrings:
            start = clock()
            s = Search(index=_index).using(self.client).query("match", content=substring)
            response = s.execute()
            end = clock() - start

            self.time = end
            self.query = substring
            self.total = response.hits.total
            self.__save__()

    def search_substrings_or(self, substrings, _index):

        start = clock()
        q = Q("match", content=substrings[0])
        for substring in substrings[1:]:
            q = q | Q("match", content=substring)

        s = Search(index=_index).using(self.client).query(q)
        response = s.execute()
        end = clock() - start
        self.time = end
        self.total = response.hits.total
        for substring in substrings[:-1]:
            self.query += "{} |".format(substring)
        self.query += substrings[-1]
        self.__save__()

    def search_substrings_and(self, substrings, _index):

        start = clock()
        q = Q("match", content=substrings[0])
        for substring in substrings[1:]:
            q = q & Q("match", content=substring)

        s = Search(index=_index).using(self.client).query(q)
        response = s.execute()
        end = clock() - start
        self.time = end
        self.total = response.hits.total
        for substring in substrings[:-1]:
            self.query += "'{}' & ".format(substring)
        self.query += substrings[-1]
        self.__save__()

    def size_of_object(self, index, field):
        s = Search(index=index).using(self.client)
        s.execute()
        s = s.scan()
        response = s
        size = 0
        for hit in response:
            size += len(hit[field])
        self.size = ((size / 1024) / 1024)
        return self.size


