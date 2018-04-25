from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import create_connection

create_connection(hosts=['localhost'])


class News(DocType):
    """
    Class for define mapping in ES
    """
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    original_id = Integer()
    published_from = Date()

    class Meta:
        index = 'news100gb'

    def save(self, **kwargs):
        return super(News, self).save(**kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from


if __name__ == '__main__':
    # create mapping in ES
    News.init()