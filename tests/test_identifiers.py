import nose.tools as n

from pickle_warehouse.identifiers import parse

cachedir = '/tmp/_'

def check_parse(index:str, path:list):
    observed = parse(cachedir, index)
    n.assert_list_equal(observed, path)

def test_parse():
    for index, path in testcases:
        yield check_parse, index, path

testcases = [
    (('a','b','c'), [cachedir, 'a', 'b', 'c']),
    (['foo','bar','baz'], [cachedir, 'foo', 'bar', 'baz']),
    ('def', [cachedir, 'def']),
    ('left/middle/right', [cachedir, 'left', 'middle', 'right']),
    ('http://thomaslevine.com/!?foo=bar', [cachedir, 'http', 'thomaslevine.com', '!?foo=bar']),
    (['http://thomaslevine.com', 'foo/bar/baz', 'a b'], [cachedir, 'http', 'thomaslevine.com', 'foo', 'bar', 'baz', 'a b']),
]
