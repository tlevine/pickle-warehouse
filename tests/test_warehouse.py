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
        path = os.path.join(self.tmp, 'how many')
        with open(path, 'wb') as fp:
            observed = pickle.dump(9001, fp)
        del(self.w['how many'])
        self.assertFalse(os.path.exists(path))

    def test_contains(self):
        self.assertFalse('needle' in self.w)
        with open(path, 'wb'):
            pass
        self.assertTrue('needle' in self.w)
