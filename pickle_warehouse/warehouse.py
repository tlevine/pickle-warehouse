import os, pickle

from pickle_warehouse.serializers import base64, identity
from pickle_warehouse.identifiers import parse as parse_identifier

try:
    FileExistsError
except NameError:
    FileExistsError = OSError

try:
    FileNotFoundError
except NameError:
    OpenError = IOError
else:
    OpenError = FileNotFoundError

try:
    FileNotFoundError
except NameError:
    DeleteError = OSError
else:
    DeleteError = FileNotFoundError

def mkdir(fn):
    'Make a directory that will contain the file.'
    try:
        os.makedirs(os.path.split(fn)[0])
    except FileExistsError:
        pass

class Warehouse:
    '''
    :param cachedir: cachedir
    :param serializer: A thing with dump and load attribute functions,
        like pickle, json, yaml,
        pickle_warehouse.base64, or pickle_warehouse.identity
    '''
    def __repr__(self):
        return 'Warehouse(%s)' % repr(self.cachedir)

    def __init__(self, cachedir, serializer = pickle):
        self.cachedir = cachedir
        self.serializer = serializer

    def filename(self, index):
        return os.path.join(self.cachedir, *parse_identifier(index))

    def __iter__(self):
        return (k for k in self.keys())

    def __setitem__(self, index, obj):
        fn = self.filename(index)
        mkdir(fn)
        with open(fn, 'wb') as fp:
            self.serializer.dump(obj, fp)

    def __getitem__(self, index):
        try:
            with open(self.filename(index), 'rb') as fp:
                item = self.serializer.load(fp)
        except OpenError as e:
            raise KeyError(*e.args)
        else:
            return item

    def __delitem__(self, index):
        path = self.filename(index)
        try:
            os.remove(path)
        except DeleteError as e:
            raise KeyError(*e.args)
        else:
            for path in _reversed_directories(self.cachedir, os.path.split(path)[0]):
                if os.listdir(path) == []:
                    os.rmdir(path)
                else:
                    break

    def __contains__(self, index):
        return os.path.isfile(self.filename(index))

    def __len__(self):
        length = 0
        for dirpath, _, filenames in os.walk(self.cachedir):
            for filename in filenames:
                length += 1
        return length

    def keys(self):
        for dirpath, _, filenames in os.walk(self.cachedir):
            for filename in filenames:
                yield os.path.relpath(os.path.join(dirpath, filename), self.cachedir)

    def values(self):
        for dirpath, _, filenames in os.walk(self.cachedir):
            for filename in filenames:
                yield self[os.path.relpath(os.path.join(dirpath, filename), self.cachedir)]

    def items(self):
        for dirpath, _, filenames in os.walk(self.cachedir):
            for filename in filenames:
                index = os.path.relpath(os.path.join(dirpath, filename), self.cachedir)
                yield index, self[os.path.relpath(os.path.join(dirpath, filename), self.cachedir)]

    def update(self, d):
        for k, v in d.items():
            self[k] = v

    def get(self, index, default = None):
        if index in self:
            return self[index]
        else:
            return default

def _reversed_directories(outer, inner):
    while outer != inner:
        yield inner
        try:
            inner = os.path.split(inner)[0]
        except OSError:
            pass
