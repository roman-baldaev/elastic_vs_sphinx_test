from matplotlib import pyplot as plt
from random import random

class GraphicInfo:

    def __init__(self, *args):
        self.test_objects = args

    def time_performance_results(self):
        """
        The method creates a graph that shows the relationship between
        the size of the test object and the search time in it.
        """
        for test in self.test_objects:
            rgb = (random(), random(), random())

