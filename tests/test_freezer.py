import unittest
from unittest.mock import (MagicMock, patch)

from src.freezer import (
    peewee,
    Freezer,
    BaseModel,
    PlatiniumBotUser,
    PlatiniumBotMessage,
    PlatiniumBotContent
)


class FreezerTestSuites(unittest.TestCase):
    """
    todo:
        [x]. in setUp() open_freezer()
        [x]. in the tearDown() close_freezer()

    FreezerTestSuites: tests the Freezer class.

    Args:
        unittest ([type]): [description]
    """
    def tearDown(self):
        self.test_freezer_obj.close_freezer()
        self.test_freezer_obj = None

    def test_open_freezer(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()

            mock_db.assert_called()

            self.test_freezer_obj.open_freezer()

            mock_db.return_value.connect.assert_called()

    def test_close_freezer(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            self.test_freezer_obj.open_freezer()
            self.test_freezer_obj.close_freezer()

            mock_db.return_value.close.assert_called()

    def test_create_bot_tables(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            self.test_freezer_obj.open_freezer()
            self.test_freezer_obj.create_bot_tables()

            mock_db.return_value.table_exists.assert_called()
            mock_db.return_value.create_tables.assert_called()

    def test_tables_existence(self):
        """
        todo:
        check if the tables are actually in the db using this method.
        """
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            self.test_freezer_obj.open_freezer()
            self.test_freezer_obj.create_bot_tables()
            tbls = self.test_freezer_obj.freezer.get_tables()

            mock_db.return_value.get_tables.assert_called_once()
            # self.assertIn("table_PlatiniumBotUser", tbls)


class PlatiniumBotUserModelTestSuites(unittest.TestCase):

    def setUp(self):
        self.platinium_bot_user = PlatiniumBotUser()
        self.platinium_bot_msg = PlatiniumBotMessage()
        self.platinium_bot_cont = PlatiniumBotContent()

    def test_models_instance_basemodel(self):
        self.assertIsInstance(self.platinium_bot_user, BaseModel)
        self.assertIsInstance(self.platinium_bot_user, peewee.Model)
        self.assertIsInstance(self.platinium_bot_msg, BaseModel)
        self.assertIsInstance(self.platinium_bot_msg, peewee.Model)
        self.assertIsInstance(self.platinium_bot_cont, BaseModel)
        self.assertIsInstance(self.platinium_bot_cont, peewee.Model)

    def test_telegramuser_tables_data(self):
        pass
