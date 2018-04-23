from abc import abstractmethod, ABC
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from time import clock
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import json

class SearchTest(ABC):

    def __init__(self, file_for_save, object_test_name=None):
        self.object_test_name = object_test_name
        self.file_for_save = file_for_save
        self.time = None
        self.results = None
        self.size = None
        self.date = None
        self.query = None
        self.total = None

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
    def __init__(self, *args, **kwargs):
        super(SearchTestElastic, self).__init__(*args, **kwargs)
        self.client = Elasticsearch(timeout=30)

    def __save__(self):
        _columns = ['index', 'size', 'query', 'time', 'total']
        data = [self.object_test_name, self.size, self.query, self.time, self.total]

        source = read_csv(self.file_for_save)
        dataframe_for_save = DataFrame([data], columns=_columns)
        _sum = concat([source, dataframe_for_save], ignore_index=True)

        _sum.to_csv(self.file_for_save, index=False)

    def search_substring(self, substrings, _index):
        # results = {}
        self.size = 3221
        self.object_test_name = _index

        for substring in substrings:

            start = clock()
            s = Search(index=_index).using(self.client).query("match", content=substring)
            response = s.execute(ignore_cache=True)

            end = clock() - start
            self.time = end
            self.query = substring
            self.total = response.hits.total
            self.__save__()

            # results[substring] = return_id

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
        length = 0
        for hit in response:
            length += 1
            print(hit.to_dict()['message'].to_dict())
        self.size = ((size / 1024) / 1024)
        return self.size

    def from_logstash_message(self, _index):
        s = Search(index=_index).using(self.client).query("match", message="hello")

        s.execute()
        s = s.scan()
        response = s

        for hit in response:
            data = json.loads(hit.message)
            print(data['content'])
