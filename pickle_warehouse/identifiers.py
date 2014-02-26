from urllib.request import urlparse
import itertools

# For Python 2 compatibility
try:
    basestring
except NameError:
    basestring = str

def parse(cachedir, index):
    if isinstance(index, basestring):
        path = [index]
    else:
        path = list(itertools.chain(map(parse_partial, index)))

    return [cachedir] + path

def parse_partial(item):
    return item
