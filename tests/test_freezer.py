import unittest
import datetime
from datetime import timezone
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
    def setUp(self):
        self.tlg_user_id = 355355326
        # self.tlg_username = None
        self.tlg_username = "Gadd"
        self.tlg_first_name = "Negassa"
        # self.tlg_phone = None
        self.tlg_phone = "+251911985365"
        self.active_status = False

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
            with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBU_model:
                if self.tlg_username is None and self.tlg_phone is None:
                    self.test_freezer_obj.add_new_bot_user(
                        self.tlg_user_id,
                        self.tlg_first_name
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=self.tlg_user_id,
                        bot_user_name=self.tlg_first_name
                    )
                    print("both username & phone ARE NONE")
                elif self.tlg_username is None and self.tlg_phone is not None:
                    self.test_freezer_obj.create_new_bot_user(
                        telegram_id=self.tlg_user_id,
                        telegram_name=self.tlg_first_name,
                        phone=self.tlg_phone
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=self.tlg_user_id,
                        bot_user_name=self.tlg_first_name,
                        bot_user_phone=self.tlg_phone
                    )
                    print("phone NOT NONE")
                elif self.tlg_phone is None and self.tlg_username is not None:
                    self.test_freezer_obj.create_new_bot_user(
                        telegram_id=self.tlg_user_id,
                        telegram_name=self.tlg_username
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=self.tlg_user_id,
                        bot_user_name=self.tlg_username
                    )
                    print("username NOT NONE")
                else:
                    self.test_freezer_obj.add_new_bot_user(
                        telegram_id=self.tlg_user_id,
                        telegram_name=self.tlg_username,
                        phone=self.tlg_phone
                    )

                    mock_PBU_model.create.assert_called_with(
                        user_telegram_id=self.tlg_user_id,
                        bot_user_name=self.tlg_username,
                        bot_user_phone=self.tlg_phone
                    )
                    print("both username & phone NOT NONE")

    # def test_update_bot_user(self):
    #     with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
    #         self.test_freezer_obj = Freezer()
    #         with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBU_model:
    #             self.test_freezer_obj.update_bot_user(active_status=self.active_status, telegram_id=self.tlg_user_id)

    #             mock_PBU_model.update.assert_called_with(active_status=self.active_status)

    def test_get_bot_user(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBU_model:
                # mock_PBU_model.select.return_value = PlatiniumBotUser(
                #     bot_user_id=1,
                #     user_telegram_id=self.tlg_user_id,
                #     bot_user_name=self.tlg_username,
                #     bot_user_phone=self.tlg_phone,
                #     bot_user_active=True,
                #     bot_user_joined_timestamp=datetime.datetime.now(
                #         tz=timezone.utc
                #     )
                # )
                mock_PBU_model.select.return_value = PlatiniumBotUser(
                    user_telegram_id=self.tlg_user_id,
                    bot_user_name=self.tlg_username,
                    bot_user_phone=self.tlg_phone
                )

                user = self.test_freezer_obj.get_bot_user(self.tlg_user_id)

                mock_PBU_model.select.assert_called_with(self.tlg_user_id)
                self.assertEqual(user.user_telegram_id, self.tlg_user_id)


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
