import os
import pickle
import tempfile
import unittest
from shutil import rmtree

import nose.tools as n

from pickle_warehouse.warehouse import Warehouse

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.w = Warehouse(self.tmp)

    def tearDown(self):
        rmtree(self.tmp)

    def test_cachedir(self):
        cachedir = self.tmp + 'aaa'
        w = Warehouse(cachedir)
        n.assert_equal(w.cachedir, cachedir)

    def test_default_dump(self):
        w = Warehouse(self.tmp)
        n.assert_equal(w.dump, pickle.dump)

    def test_repr(self):
        self.assertEqual(repr(self.w), "Warehouse('%s')" % self.tmp)
        self.assertEqual(str(self.w), "Warehouse('%s')" % self.tmp)

        self.assertEqual(str(Warehouse('/tmp/a"b"c"')), '''Warehouse('/tmp/a"b"c"')''')

    def test_setitem(self):
        self.w[("Tom's", 'favorite color')] = 'pink'
        with open(os.path.join(self.tmp, "Tom's", 'favorite color'), 'rb') as fp:
            observed = pickle.load(fp)
        self.assertEqual(observed, 'pink')

    def test_setitem_dump(self):
        content = 'pink'
        def fake_dump(obj, fp):
            self.assertEqual(obj, content)
        self.w.dump = fake_dump
        self.w[("Tom's", 'favorite color')] = 'pink'

    def test_getitem(self):
        with open(os.path.join(self.tmp, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        self.assertEqual(self.w['profession'], 'dada artist')

        with self.assertRaises(KeyError):
            self.w['not a file']

    def test_get(self):
        with open(os.path.join(self.tmp, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        self.assertEqual(self.w['profession'], 'dada artist')
        self.assertEqual(self.w.get('hobby','business intelligence'), 'business intelligence')

    def test_delitem1(self):
        dirname = os.path.join(self.tmp, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        del(self.w[['foo','bar']])
        self.assertFalse(os.path.exists(filename))
        self.assertFalse(os.path.exists(dirname))

        with self.assertRaises(KeyError):
            del(self.w['not a file'])

    def test_delitem2(self):
        dirname = os.path.join(self.tmp, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        with open(filename+'2', 'wb') as fp:
            pass
        del(self.w[['foo','bar']])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(dirname))

        with self.assertRaises(KeyError):
            del(self.w['not a file'])

    def test_contains(self):
        self.assertFalse('needle' in self.w)
        with open(os.path.join(self.tmp, 'needle'), 'wb'):
            pass
        self.assertTrue('needle' in self.w)

    def test_len(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.tmp, 'z'), 'wb'):
            pass
        self.assertEqual(len(self.w), 2)

    def test_update(self):
        self.w.update({'dictionary': {'a':'z'}})
        with open(os.path.join(self.tmp, 'dictionary'), 'rb') as fp:
            observed = pickle.load(fp)
        self.assertEqual(observed, {'a':'z'})

    def test_iter(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.tmp, 'z'), 'wb'):
            pass

        observed = set(x for x in self.w)
        expected = {'a/b/c/d', 'z'}

        n.assert_set_equal(observed, expected)

    def test_keys(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb'):
            pass
        with open(os.path.join(self.tmp, 'z'), 'wb'):
            pass

        observed = set(self.w.keys())
        expected = {'a/b/c/d', 'z'}

        n.assert_set_equal(observed, expected)

    def test_values(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb') as fp:
            pickle.dump(123, fp)
        with open(os.path.join(self.tmp, 'z'), 'wb') as fp:
            pickle.dump(str, fp)

        observed = set(self.w.values())
        expected = {123,str}

        n.assert_set_equal(observed, expected)

    def test_items(self):
        abc = os.path.join(self.tmp, 'a', 'b', 'c')
        os.makedirs(abc)
        with open(os.path.join(abc, 'd'), 'wb') as fp:
            pickle.dump(9, fp)
        with open(os.path.join(self.tmp, 'z'), 'wb') as fp:
            pickle.dump(str, fp)

        observed = set(self.w.items())
        expected = {('a/b/c/d',9), ('z',str)}

        n.assert_set_equal(observed, expected)


def test_mkdir():
    d = '/tmp/not a directory'
    w = Warehouse(d)
    if os.path.exists(d):
        rmtree(d)
    w[('abc','def','ghi')] = 3
    with open(os.path.join('/tmp/not a directory/abc/def/ghi'), 'rb') as fp:
        observed = pickle.load(fp)
    n.assert_equal(observed, 3)
