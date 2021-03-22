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

    FreezerTestSuites: tests the Freezer class.

    Args:
        unittest (TestCase): A class whose instances are single test cases that are inherited.
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
            mock_db.side_effect = peewee.PeeweeException
            self.test_freezer_obj.open_freezer()
            self.test_freezer_obj.close_freezer()

            mock_db.return_value.close.assert_called()

    def test_create_bot_tables(self):
        # hack remember that whenever you act on a mock it always returns a mock, thus when you call table_exists
        # on the mock it returns true and continues on executing the code. What you need to do is find a way to make
        # mock_db as realistic as possible by populating it with whatever you're testing and the proceed from that.
        # todo find a way to get a full db into the mock
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            mock_db.side_effect = peewee.PeeweeException
            self.test_freezer_obj.freezer.table_exists.return_value = False
            self.test_freezer_obj.create_bot_tables()

            mock_db.return_value.table_exists.assert_called_with(
                "table_PlatiniumBotMessage"
            )
            mock_db.return_value.create_tables.assert_called()
            mock_db.return_value.create_tables.assert_called_with(
                [PlatiniumBotUser, PlatiniumBotContent, PlatiniumBotMessage]
            )

    def test_tables_existence(self):
        """
        todo:
        check if the tables are actually in the db using this method.
        """
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            mock_db.side_effect = peewee.PeeweeException
            self.test_freezer_obj.create_bot_tables()

            self.test_freezer_obj.freezer.get_tables.return_value = [
                'table_PlatiniumBotUser',
                'table_PlatiniumBotContent',
                'table_PlatiniumBotMessage'
            ]
            tbls = self.test_freezer_obj.freezer.get_tables()
            self.assertIn("table_PlatiniumBotUser", tbls)


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
