from matplotlib import pyplot as plt
from random import random
from pandas import read_csv
from numpy import mean
import matplotlib as plt


class GraphicInfo:
    """
    This class displays the results of the search queries tests.
    When initialized, it takes a list of CSV files (*args) with the results.
    Each file for a separate search engine (or database) with the following column names:
    'index', 'date', 'percent', 'query', 'time', 'size'(MB)
    """
    def __init__(self, *args):
        self.results_csv = args

    def time_performance_results(self):
        """
        The method creates a graph that shows the relationship between
        the size of the test object and the search time in it.
        """
        for csv in self.results_csv:
            data_results = read_csv(csv)
            rgb = (random(), random(), random())
            sizes = list(set(data_results['size'])).sort()
            for size in sizes:
                times = []
                time = mean(data_results['size' == size, 'time'])
                times.append(time)
            plt.plot(sizes, times, color=rgb, label=csv[:-4])
        plt.show()
