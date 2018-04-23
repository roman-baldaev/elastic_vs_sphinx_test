from elasticsearch import helpers, Elasticsearch
import csv


if __name__ == "__main__":

    es = Elasticsearch()
    with open('/home/roman/Projects/ElasticMongoTest/src/news-kaggle/datasets/articles1.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        helpers.bulk(es, reader, stats_only=True, index='news10gb', doc_type='News')