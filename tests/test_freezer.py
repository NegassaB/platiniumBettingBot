import unittest
from unittest.mock import (MagicMock, patch)

from src.freezer import (
    peewee,
    Freezer,
    BaseFarm,
    PlatiniumBotUser,
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
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            mock_db.side_effect = peewee.PeeweeException
            self.test_freezer_obj.freezer.table_exists.return_value = False
            self.test_freezer_obj.create_bot_tables()

            mock_db.return_value.table_exists.assert_called_with(
                "table_PlatiniumBotContent"
            )
            mock_db.return_value.create_tables.assert_called()
            # turns out the return_value from mock_db is actually test_freezer.obj.freezer itself
            # self.test_freezer_obj.freezer.create_tables.assert_called()
            mock_db.return_value.create_tables.assert_called_with(
                [PlatiniumBotUser, PlatiniumBotContent]
            )

    def test_create_new_bot_user(self):
        with patch("src.freezer.peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            tlg_user_id = 355355326
            # tlg_username = None
            tlg_username = "Gadd"
            tlg_first_name = "Negassa"
            # tlg_phone = None
            tlg_phone = "+251911985365"
            with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBU_model:
                if tlg_username is None and tlg_phone is None:
                    self.test_freezer_obj.create_new_bot_user(
                        tlg_user_id,
                        tlg_first_name
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=tlg_user_id,
                        bot_user_name=tlg_first_name
                    )
                    print("both username & phone ARE NONE")
                elif tlg_username is None and tlg_phone is not None:
                    self.test_freezer_obj.create_new_bot_user(
                        telegram_id=tlg_user_id,
                        telegram_name=tlg_first_name,
                        phone=tlg_phone
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=tlg_user_id,
                        bot_user_name=tlg_first_name,
                        bot_user_phone=tlg_phone
                    )
                    print("phone NOT NONE")
                elif tlg_phone is None and tlg_username is not None:
                    self.test_freezer_obj.create_new_bot_user(
                        telegram_id=tlg_user_id,
                        telegram_name=tlg_username
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=tlg_user_id,
                        bot_user_name=tlg_username
                    )
                    print("username NOT NONE")
                else:
                    self.test_freezer_obj.create_new_bot_user(
                        telegram_id=tlg_user_id,
                        telegram_name=tlg_username,
                        phone=tlg_phone
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=tlg_user_id,
                        bot_user_name=tlg_username,
                        bot_user_phone=tlg_phone
                    )
                    print("both username & phone NOT NONE")


class PlatiniumBotUserModelTestSuites(unittest.TestCase):

    def setUp(self):
        self.platinium_bot_user = PlatiniumBotUser()
        self.platinium_bot_content = PlatiniumBotContent()

    def test_models_instance_basemodel(self):
        self.assertIsInstance(self.platinium_bot_user, BaseFarm)
        self.assertIsInstance(self.platinium_bot_user, peewee.Model)
        self.assertIsInstance(self.platinium_bot_content, BaseFarm)
        self.assertIsInstance(self.platinium_bot_content, peewee.Model)

    def test_telegramuser_tables_data(self):
        pass
