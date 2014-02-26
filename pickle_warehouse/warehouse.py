import os, pickle

from pickle_warehouse.identifiers import parse as parse_identifier

class Warehouse:
    def __init__(self, cachedir):
        self.cachedir = cachedir

    def __setitem__(self, index, obj):
        fn = os.path.join(self.cachedir, *parse_identifier(index))
        with open(fn, 'wb') as fp:
            pickle.dump(obj, fp)
