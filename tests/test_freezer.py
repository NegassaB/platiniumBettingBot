import unittest
from unittest.mock import MagicMock, patch

from src.freezer import Freezer


class FreezerTestSuites(unittest.TestCase):
    """
    todo:
        1. in setUp() open_freezer()
        2. in the tearDown() close_freezer()
        3. based on the above test Freezer()

    FreezerTestSuites: tests the Freezer class.

    Args:
        unittest ([type]): [description]
    """
    def setUp(self):
        self.freezer = Freezer()

    # def tearDown(self):
    #     self.freezer.close()

    def test_open_freezer(self):
        self.assertTrue(self.freezer.open_freezer())

    def test_close_freezer(self):
        self.freezer.open_freezer()
        self.assertTrue(self.freezer.close_freezer())
