from urllib.request import urlsplit
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
        path = list(itertools.chain(*map(parse_partial, index)))

    return [cachedir] + path

def parse_partial(item):
    x = urlsplit(item)

    if x.scheme:
        yield x.scheme

    if x.netloc:
        yield x.netloc

    if x.path:
        for y in filter(None, path.split('/')):
            yield y

    rightmost = ''
    if x.query:
        rightmost += '?' + x.query
    if x.fragment:
        rightmost += '#' + x.fragment
    if rightmost:
        yield rightmost
