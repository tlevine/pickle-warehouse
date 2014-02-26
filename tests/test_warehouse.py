import tempfile
import unittest

import nose.tools as n

from pickle_warehouse import Warehouse

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.w = Warehouse(self.tmp)

    def check_parse(self, index:str, path:list):
        observed = self.parse(index)
        n.assert_list_equal(observed, expected)

    def test_parse_tuple(self):
        self.check_parse(('a','b','c'), [self.tmp, 'a', 'b', 'c'])

    def test_parse_list(self):
        self.check_parse(['foo','bar','baz'], [self.tmp, 'foo', 'bar', 'baz'])

    def test_parse_list(self):
        self.check_parse('def', [self.tmp, 'def'])

    def test_parse_slashes(self):
        self.check_parse('left/middle/right', [self.tmp, 'left', 'middle', 'right'])

    def test_parse_url(self):
        self.check_parse('http://thomaslevine.com/!?foo=bar', [self.tmp, 'http', 'thomaslevine.com', '!?foo=bar'])

    def test_parse_combination(self):
        index = ['http://thomaslevine.com', 'foo/bar/baz', 'a b']
        path = ['http', 'thomaslevine.com', 'foo', 'bar', 'baz', 'a b']
        self.check_parse(index, path)
