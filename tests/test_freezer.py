import unittest
from unittest.mock import (MagicMock, patch)

import peewee

from src.freezer import (Freezer, BaseModel, TelegramUser)


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


class BaseModelTestSuites(unittest.TestCase):

    def test_telegramuser_instance_basemodel(self):
        self.telegram_user = TelegramUser()
        self.assertIsInstance(self.telegram_user, BaseModel)
        self.assertIsInstance(self.telegram_user, peewee.Model)
