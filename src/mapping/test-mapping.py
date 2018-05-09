from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, InnerDoc, Integer, Keyword, Text, Nested, Object
from elasticsearch_dsl.connections import create_connection

create_connection(hosts=['localhost'])

"""
    With this code, try to implement a rather complex mapping in Elastic.
"""


class Entity(InnerDoc):
    """
        Inner mapping for define 'entity' attribute in the main class 'Document'
    """
    keyword = Text(fields={'raw': Keyword()})

    # 'index' attribute consists of two attributes
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
        This class partially aggregates the above classes, using them as attributes.

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
    """
        To create a mapping, you need to use 'mapping_name'.init()
        For this example: Document.init()
        The code below shows the process of adding a document using a previously defined mapping as a class. 
    """
    client = Elasticsearch()

    a = [5, 10, 21, 345]
    _keywords = ['hello', 'world', 'AI', 'Great', 'Britain']

    first = Document(
            keywords=_keywords,
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

