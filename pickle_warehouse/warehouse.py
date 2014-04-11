import os, pickle

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
        like pickle, json, yaml, dill, bson, 
        or anything in pickle_warehouse.serializers
    '''
    def __repr__(self):
        return 'Warehouse(%s)' % repr(self.cachedir)

    def __init__(self, cachedir, serializer = pickle, mutable = True):
        self.cachedir = cachedir
        self.serializer = serializer
        self.mutable = mutable

    def filename(self, index):
        return os.path.join(self.cachedir, *parse_identifier(index))

    def __iter__(self):
        return (k for k in self.keys())

    def __setitem__(self, index, obj):
        fn = self.filename(index)
        mkdir(fn)
        if (not self.mutable) and os.path.exists(fn):
            raise PermissionError('This warehouse is immutable, and %s already exists.' % fn)
        else:
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
        if not self.mutable:
            raise PermissionError('This warehouse is immutable, so you can\'t delete things.')

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
