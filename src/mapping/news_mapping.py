from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import create_connection

create_connection(hosts=['localhost'])


class News(DocType):
    """
    Class for define mapping in ES
    """
    id = Integer()
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    publication = Text(analyzer='snowball', fields={'raw': Keyword()})
    author = Text(analyzer='snowball', fields={'raw': Keyword()})
    date = Date()
    year = Integer()
    month = Text(analyzer='snowball', fields={'raw': Keyword()})
    url = Text(analyzer='snowball', fields={'raw': Keyword()})
    content = Text(analyzer='snowball')


    class Meta:
        index = 'news14gb'

    def save(self, **kwargs):
        return super(News, self).save(**kwargs)


if __name__ == '__main__':
    # create mapping in ES
    News.init()