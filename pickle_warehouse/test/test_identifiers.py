import datetime

import nose.tools as n

from pickle_warehouse.identifiers import parse, parse_partial

#def check_parse(index:str, path:list):
def check_parse(index, path):
    observed = parse(index)
    n.assert_list_equal(observed, path)

def test_parse():
    for index, path in testcases:
        yield check_parse, index, path

def test_parse_url():
    o = list(parse_partial('http://thomaslevine.com/!/about?a=b#lala'))
    e = ['http', 'thomaslevine.com', '!', 'about?a=b#lala']
    n.assert_list_equal(o, e)

def test_parse_date():
    o = list(parse_partial(datetime.date(2014, 2, 5)))
    e = ['2014', '02', '05']
    n.assert_list_equal(o, e)

def test_parse_datetime():
    o = list(parse_partial(datetime.datetime(2014, 2, 5, 11, 18, 30)))
    e = ['2014', '02', '05']
    n.assert_list_equal(o, e)

testcases = [
    (('a','b','c'), ['a', 'b', 'c']),
    (['foo','bar','baz'], ['foo', 'bar', 'baz']),
    ('def', ['def']),
    ('favorite color', ['favorite color']),
    ('left/middle/right', ['left', 'middle', 'right']),
    ('backslashes\\also\\delimit', ['backslashes','also','delimit']),
    ('/home/tlevine/warehouse', ['home', 'tlevine', 'warehouse']),
    ('C:\\Users\\Documents', ['C:', 'Users', 'Documents']),
    ('http://thomaslevine.com/!?foo=bar', ['http', 'thomaslevine.com', '!?foo=bar']),
    (['http://thomaslevine.com', 'foo/bar/baz', 'a b'], ['http', 'thomaslevine.com', 'foo', 'bar', 'baz', 'a b']),
]
