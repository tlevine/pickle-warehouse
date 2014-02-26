import os
import pickle
import tempfile
import unittest
from shutil import rmtree

from pickle_warehouse.warehouse import Warehouse

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.w = Warehouse(self.tmp)

    def tearDown(self):
        rmtree(self.tmp)

    def test_setitem(self):
        self.w['favorite color'] = 'pink'
        with open(os.path.join(self.tmp, 'favorite color'), 'rb') as fp:
            observed = pickle.load(fp)
        self.assertEqual(observed, 'pink')

    def test_getitem(self):
        with open(os.path.join(self.tmp, 'profession'), 'wb') as fp:
            observed = pickle.dump('dada artist', fp)
        self.assertEqual(self.w['profession'], 'dada artist')

    def test_delitem(self):
        dirname = os.path.join(self.tmp, 'foo')
        filename= os.path.join(dirname, 'bar')
        os.mkdir(dirname)
        with open(filename, 'wb') as fp:
            pass
        del(self.w[['foo','bar']])
        self.assertFalse(os.path.exists(filename))
        self.assertFalse(os.path.exists(dirname))

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
