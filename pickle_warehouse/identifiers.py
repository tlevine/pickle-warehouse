from urllib.request import urlsplit
import itertools

# For Python 2 compatibility
try:
    basestring
except NameError:
    basestring = str

def parse(cachedir, index):
    if isinstance(index, basestring):
        path = list(parse_partial(index))
    else:
        path = list(itertools.chain(*map(parse_partial, index)))

    return [cachedir] + path

def parse_partial(item):
    url = urlsplit(item)
    path = []

    if url.scheme:
        path.append(url.scheme)

    if url.netloc:
        path.append(url.netloc)

    if url.path:
        for y in filter(None, url.path.split('/')):
            path.append(y)

    if url.query:
        path[-1] += '?' + url.query

    if url.fragment:
        path[-1] += '#' + url.fragment

    return path
