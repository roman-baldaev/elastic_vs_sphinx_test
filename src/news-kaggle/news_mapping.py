from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

connections.create_connections(hosts=['localhost'])


class ArticleNews(DocType):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    author = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    published_from = Date()

    class Meta:
        index = 'news'

    def save(self, **kwargs):
        return super(ArticleNews, self).save(**kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from


if __name__ == '__main__':
    # create mapping in ES
    ArticleNews.init()