import tempfile
import unittest

import nose.tools as n

from pickle_warehouse import Warehouse

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.w = Warehouse(self.tmp)

    def test_set(self):
        self.w
