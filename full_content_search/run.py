'''
    pip install whoosh -i https://pypi.douban.com/simple
'''

import os
from whoosh.fields import TEXT, ID, Schema
from whoosh.index import open_dir, create_in
from whoosh.qparser import QueryParser


# 判断是否含有中文
def is_contains_chinese(strs):
    for c in strs:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False


class FullSearchFactory:

    _instance = {}

    def __new__(cls, *args, **kw):
        if not cls._instance.get(cls):
            cls._instance[cls] = super().__new__(cls)
        return cls._instance[cls]

    def __init__(self):
        self.schema = Schema(title=TEXT(stored=True),
                             path=ID(stored=True),
                             content=TEXT(stored=True))
        self._index_dir = self._index_dir

        if os.path.exists(self._index_dir):
            os.mkdir(self._index_dir)

    def query(self, keyword):
        ix = open_dir(self._index_dir)
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(" ".join(keyword))
            results = searcher.search(query)
            if results:
                print(results)

    def add(self, title="", content=None, file=None, dir_=None, path=""):
        ix = open_dir(self._index_dir)
        writer = ix.writer()
        if content:
            writer.add_document(title=title, path=path, content=content)
            return

        if file:
            title = os.path.basename(file)
            with open(file, "r") as f:
                writer.add_document(title=title, path=file, content=f.read())
            return

        for root, _, files in os.walk(dir_):
            for fl in files:
                path = os.path.join(root, fl)
                with open(path, "r") as f:
                    writer.add_document(title=fl, path=path, content=f.read())


def manage():
    # with open(os.path.join(os.getcwd(), "test.txt"), "r") as f:
    #     content = f.read()
    #     print(content, type(content))

    a = os.path.basename("c:/das/r.txt")

    for a, b, c in os.walk("D:\\code\\flask-internal\\"):
        print(a, b, c)
    # print(a)


if __name__ == '__main__':
    # test()
    # query()
    manage()
