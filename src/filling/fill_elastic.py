from pandas import read_csv
from mapping.news_mapping import News
from elasticsearch_dsl.connections import create_connection

# create_connection(hosts=['localhost'], timeout=1000000)
#
#
# def fill_from_csv(file_path):
#     """
#     Method for saving data from a file to ES by saving an instance of a class
#     :param file_path: path to CSV-file
#     """
#     data = read_csv(file_path)
#     n = len(data)
#     for j in range(1000):
#         for i in range(21000, n):
#             item = data.iloc[i, :]
#
#             news = News(title=item['title'],
#                         content=item['content'],
#                         )
#             news.original_id = int(item['id'])
#             news.save()
#             print("Part: {} News: {}".format(j, i))
#     return 0
#
# if __name__=="__main__":
#     #simple test
#     fill_from_csv('/home/roman/Projects/ElasticMongoTest/src/news-kaggle/datasets/articles3.csv')
