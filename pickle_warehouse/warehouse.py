import os, pickle

from pickle_warehouse.identifiers import parse as parse_identifier

class Warehouse:
    def __init__(self, cachedir):
        self.cachedir = cachedir

    def filename(self, index):
        return os.path.join(self.cachedir, *parse_identifier(index))

    def __setitem__(self, index, obj):
        with open(self.filename(index), 'wb') as fp:
            pickle.dump(obj, fp)

    def __getitem__(self, index):
        with open(self.filename(index), 'rb') as fp:
            item = pickle.load(fp)
        return item

    def __delitem__(self, index):
        path = self.filename(index)
        os.remove(path)
        for path in _reversed_directories(self.cachedir, os.path.split(path)[0]):
            os.rmdir(path)

def _reversed_directories(outer, inner):
    while outer != inner:
        yield inner
        try:
            inner = os.path.split(inner)[0]
        except OSError:
            pass
