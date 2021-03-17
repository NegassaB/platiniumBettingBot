import unittest
from unittest.mock import (MagicMock, patch)

from src.freezer import (Freezer, BaseModel, PlatiniumBotUser, peewee)


class FreezerTestSuites(unittest.TestCase):
    """
    todo:
        [x]. in setUp() open_freezer()
        [x]. in the tearDown() close_freezer()

    FreezerTestSuites: tests the Freezer class.

    Args:
        unittest ([type]): [description]
    """
    def test_open_freezer(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.freezer = Freezer()
            mock_db.assert_called()
            self.freezer.open_freezer()
            mock_db.return_value.connect.assert_called()

    def test_close_freezer(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.freezer = Freezer()
            self.freezer.open_freezer()
            self.freezer.close_freezer()
            mock_db.return_value.close.assert_called()


class PlatiniumBotUserModelTestSuites(unittest.TestCase):

    def setUp(self):
        self.platinium_bot_user = PlatiniumBotUser()

    def test_telegramuser_instance_basemodel(self):
        self.assertIsInstance(self.platinium_bot_user, BaseModel)
        self.assertIsInstance(self.platinium_bot_user, peewee.Model)

    def test_telegramuser_tables_data(self):
        pass
