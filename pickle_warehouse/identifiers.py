from urllib.request import urlsplit
import itertools
import datetime

# For Python 2 compatibility
try:
    basestring
except NameError:
    basestring = str

def parse(cachedir, index):
    for theclass in [basestring, datetime.date, datetime.datetime]:
        if isinstance(index, theclass):
            path = list(parse_partial(index))
            break
    else:
        path = list(itertools.chain(*map(parse_partial, index)))

    return [cachedir] + path

def parse_partial(item):
    if isinstance(item, basestring):
        func = parse_partial_url
    elif isinstance(item, datetime.date) or isinstance(item, datetime.datetime):
        func = parse_partial_date
    else:
        raise ValueError('item must be string, datetime.date or datetime.datetime')
    return func(item)

def parse_partial_url(item):
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

def parse_partial_date(item):
    return ['%04d' % item.year, '%02d', item.month, '%02d', item.day]
