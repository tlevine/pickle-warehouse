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

    def test_set_item(self):
        self.w['favorite color'] = 'pink'
        with open(os.path.join(self.tmp, 'favorite color'), 'rb') as fp:
            observed = pickle.load(fp)
        self.assertEqual(observed, 'pink')

    def test_get_item(self):
        with open(os.path.join(self.tmp, 'favorite color'), 'wb') as fp:
            observed = pickle.dump('pink', fp)
        self.assertEqual(self.w['favorite color'], 'pink')
