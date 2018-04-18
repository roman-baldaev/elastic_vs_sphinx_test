from gensim.corpora import WikiCorpus
import os
from lxml import etree
from io import StringIO

if __name__ == '__main__':
    path = r"C:\Users\roman.baldaev\PycharmProjects\ElasticSearchTest\src\wiki\datasets"
    file_name = os.path.join(path, "enwiki-latest-pages-articles10.xml-p2336425p3046511")
    tree = etree.parse(file_name)

    raws = tree.xpath('/page')
    print(len(raws))
    for raw in raws:
        print(raw.xpath('/text').text)
