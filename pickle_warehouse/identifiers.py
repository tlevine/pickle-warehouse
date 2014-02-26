import types

from urllib.request import urlparse

def parse(cachedir, index):
    if isinstance(index, types.StringTypes):
        path = [index]
    else:
        path = list(itertools.chain(map(parse_partial, index)))

    return [cachedir] + path

def parse_partial(item):
    return item
