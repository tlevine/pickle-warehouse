from pickle_warehouse.identifiers import parse as parse_identifier

class Warehouse:
    def __init__(self, cachedir):
        self.cachedir = cachedir

    def __setitem__(self, index, obj):
        parse_identifier(index)
