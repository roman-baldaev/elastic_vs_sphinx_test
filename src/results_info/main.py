from graphic_info import GraphicInfo


if __name__ == "__main__":
    """
    Simple test for GraphicInfo module
    """
    info = GraphicInfo(r"C:\Users\roman.baldaev\PycharmProjects\ElasticVsMongoTest\elastic_vs_mongodb_test\test_results_csv",
                   r"ElasticsearchTest.csv")

    info.time_performance_results()