import unittest
from unittest.mock import MagicMock, patch

from src.freezer import Freezer


class FreezerTestSuites(unittest.TestCase):
    """
    todo:
        [x]. in setUp() open_freezer()
        [x]. in the tearDown() close_freezer()

    FreezerTestSuites: tests the Freezer class.

    Args:
        unittest ([type]): [description]
    """
    def setUp(self):
        self.freezer = Freezer()
        self.freezer.open_freezer()

    def tearDown(self):
        self.freezer.close_freezer()
        self.freezer = None

    def test_create_table(self):
        pass

    def test_insert_a_record(self):
        pass
