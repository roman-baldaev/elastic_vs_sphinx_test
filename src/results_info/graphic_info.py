from matplotlib import pyplot as plt
from random import random
from pandas import read_csv
from numpy import mean, sort
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os.path import join


class GraphicInfo:
    """
    This class displays the results of the search queries tests.
    When initialized, it takes a list of CSV files (*args) with the results.
    'path' is the name of the directory where the CSV files with tests results are contained.
    Each file for a separate search engine (or database) with the following column names:
    'index', 'query', 'time', 'size'(MB)
    """
    def __init__(self, path, *args):
        self.results_csv = args
        self.path = path

    def time_performance_results(self):
        """
        The method creates a graph that shows the relationship between
        the size of the test object and the search time in it.
        """
        for csv in self.results_csv:
            # absolute path to CSV
            path = join(self.path, csv)
            data_results = read_csv(path)

            # random color for each result
            rgb = (random(), random(), random())

            # sorted by an array of unique values of the size of the test data
            sizes = sort(list(set(data_results['size'])))

            # calculate the average search time for each test data size
            for _size in sizes:
                times = []
                mean_time = mean(data_results[data_results['size'] == _size].time)
                times.append(mean_time)

            # 'label' is the name of the file without an extension
            label = mpatches.Patch(color=rgb, label=csv[:-4])
            plt.legend(handles=[label])
            plt.plot(sizes, times, color=rgb)
        plt.show()
