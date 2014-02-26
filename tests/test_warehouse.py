import tempfile
import unittest

from pickle_warehouse.warehouse import Warehouse

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.w = Warehouse(self.tmp)

    def test_set_item(self):
        self.w['favorite color'] = 'pink'
        with open(os.path.join(self.tmp, 'favorite color', 'rb')) as fp:
            observed = pickle.load(fp)
        expected = pickle.dumps('pink')
        self.assertEqual(observed, expected)
