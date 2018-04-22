from abc import abstractmethod, ABC
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from time import clock
from pandas import read_csv
from pandas import DataFrame
from pandas import concat


class SearchTest(ABC):

    def __init__(self, object_test_name, file_for_save):
        self.object_test_name = object_test_name
        self.file_for_save = file_for_save
        self.time = None
        self.results = None
        self.size = None
        self.date = None
        self.query = None

    @property
    @classmethod
    def test_name(cls):
        return cls.__name__

    @abstractmethod
    def search_substring(self, substrings, field):
        ...

    @property
    @abstractmethod
    def test_results(self):
        ...

    @abstractmethod
    def show_results(self):
        ...

    @property
    @abstractmethod
    def size_of_object(self):
        ...


class SearchTestElastic(SearchTest):
    """
    'object_test_name' for Elasticsearch its name of index
    'path_to_object' is the address of the server
    """
    def __init__(self):
        self.client = Elasticsearch()

    def __save__(self):
        _columns = ['index', 'size', 'query', 'time', 'date', 'percent']
        data = [self.object_test_name, self.size, self.query, self.time, '52%']

        source = read_csv(self.file_for_save)
        dataframe_for_save = DataFrame([data], columns=_columns)
        _sum = concat([source, dataframe_for_save], ignore_index=True)

        _sum.to_csv(self.file_for_save, index=False)

    def search_substring(self, substrings, _index):
        # results = {}

        for substring in substrings:
            return_id = []
            start = clock()
            s = Search().using(self.client, index=_index).query("match", content=substring)
            end = clock() - start
            self.time = end
            # response = s.execute()
            for hit in s.scan():
                return_id.append(hit.original_id)
            results[substring] = return_id

        # self.results = results

    def search_substrings_or(self, substrings):

        start = clock()
        q = Q("match", content=substrings[0])
        for substring in substrings[1:]:
            q = q | Q("match", content=substring)
        s = Search().using(self.client).query(q)
        s.execute()
        end = clock() - start
        i = 0
        a = []
        for hit in s.scan():
            print(hit.original_id)
            a.append(hit.original_id)
            i += 1
        print("Len {}".format(len(a)))
        print(end)

    def show_results(self):
        if self.times and self.results:
            print(self.results)
            print(self.times)

    def test_results(self):
        if (self.times is not None) and (self.results is not None):
            return self.times, self.results

    def size_of_object(self, _index):
        s = Search(index=_index).using(self.client)

        s.execute()
        s = s.scan()
        response = s
        size = 0
        for hit in response:
            size += len(hit.content)
        self.size = ((size/1024)/1024)
