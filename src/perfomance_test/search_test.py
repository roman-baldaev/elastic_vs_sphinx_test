from abc import abstractmethod, ABC
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from time import clock
import pandas as pd


class SearchTest(ABC):

    def __init__(self, object_test_name, path_to_object):
        self.object_test_name = object_test_name
        self.path_to_object = path_to_object
        self.client = Elasticsearch()
        self.times = None
        self.results = None
        self.size = None

        self.hash_results = None

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

    @property
    @abstractmethod
    def distribution_size_of_docs(self):
        ...

    @abstractmethod
    def show_results(self):
        ...

    @property
    @abstractmethod
    def size_of_object(self):
        ...

# class ElastisearchTest(SearchTest):


class SearchTestElastic(SearchTest):
    """
    'object_test_name' for Elasticsearch its name of index
    'path_to_object' is the address of the server
    """
    def search_substring(self, substrings, _field):
        # will do DataFrame object
        times = []
        results = {}
        for substring in substrings:
            return_id = []
            start = clock()
            s = Search().using(self.client).query("match", content=substring)
            end = clock() - start
            times.append(end)
            response = s.execute()
            print(response)
            for hit in s.scan():
                return_id.append(hit.original_id)
            results[substring] = return_id
        self.times = times
        self.results = results

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

    def size_of_object(self):
        s = Search(index=self.object_test_name).using(self.client)

        s.execute()
        s = s.scan()
        response = s
        size = 0
        for hit in response:
            size += len(hit.content)
        self.size = ((size/1024)/1024)

    def distribution_size_of_docs(self):
        return 0