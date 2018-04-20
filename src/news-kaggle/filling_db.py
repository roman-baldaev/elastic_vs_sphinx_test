from pandas import read_csv
from news_mapping import News
from elasticsearch_dsl.connections import create_connection

create_connection(hosts=['localhost'], timeout=10000)

def fill_from_csv(file_path):

    data = read_csv(file_path)
    n = len(data)
    for j in range(500):
        for i in range(n):
            item = data.iloc[i, :]

            news = News(title=item['title'],
                        content=item['content'],
                        published_from=item['date'])
            news.original_id = int(item['id'])
            news.save()
            print("Part: {} News: {}".format(j, i))
    return 0


fill_from_csv('/home/roman/Projects/ElasticMongoTest/src/news-kaggle/datasets/articles2.csv')
