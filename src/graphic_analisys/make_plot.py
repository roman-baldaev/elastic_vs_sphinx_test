from matplotlib import pyplot as plt


class GraphicInfo():

    def __init__(self, *args):
        self.time_tests = args

    def time_size_relationship(self):
        for test in self.time_tests
            plt.plot(test, times)