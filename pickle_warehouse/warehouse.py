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
        os.path.remove(self.filename(index))
