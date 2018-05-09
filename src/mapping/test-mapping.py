from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, InnerDoc, Date, Integer, Keyword, Text, Nested, Search, Object
from elasticsearch_dsl.connections import create_connection

create_connection(hosts=['localhost'])


class Entity(InnerDoc):
    """
    Inner mapping for define 'entity' attribute in the main class 'Document'
    """
    keyword = Text(fields={'raw': Keyword()})

    # index consists of two attributes
    # (arrays with a mixture of datatypes are not supported in ES)
    index = Nested(
        properties={
            'indexes': Integer(multi=True),
            'words': Text(fields={'raw': Keyword()})
        }
    )


class Coreferenc(InnerDoc):
    """
        Inner mapping for define 'coreferenc' attribute in the main class 'Document'
    """
    cluster_info = Nested(
        properties={
                'cluster_name': Text(fields={'raw': Keyword()}),
                'words': Text(fields={'raw': Keyword()}),
                'indexes': Integer(multi=True)
        }
    )


class Document(DocType):
    """
    Class for define mapping in ES
    """

    keywords = Text(fields={'raw': Keyword()})
    entity = Nested(Entity)
    cluster = Object(Coreferenc)
    type = Integer()

    class Meta:
        index = 'hard_mapping'

    def save(self, **kwargs):
        return super(Document, self).save(**kwargs)


if __name__ == '__main__':
    client = Elasticsearch()
    # create mapping in ES
    # Document.init()
    a = [5, 10]
    first = Document(keywords=['hello', 'world', 'AI', 'Great', 'Britain'],
                    type=345,
                    entity={'keyword': 'person',
                            'index': {
                                'range': a
                            }
                        },
                    cluster=[
                        {
                            'cluster_name': 'langs',
                            'words': ['Java', 'Ruby', 'Haskell'],
                            'indexes': [23, 23, 90]
                        },
                        {
                            'cluster_name': 'patterns',
                            'words': ['Singleton', 'Factory', 'Decorator'],
                            'indexes':[1, 2, 3]
                        }
                    ]
                )
    first.meta.id = 2
    first.save()
    s = Search(index='hard_mapping')
    results = s.execute()
    for doc in results:
        print(doc)