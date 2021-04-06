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
        self.tlg_active_status = False

    def tearDown(self):
        self.test_freezer_obj.close_freezer()
        self.test_freezer_obj = None

    def test_open_freezer(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()

            mock_db.assert_called()

            self.test_freezer_obj.open_freezer()

            mock_db.return_value.connect.assert_called()
            self.assertTrue(self.test_freezer_obj.db_open)

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

    """
    def test_update_bot_user(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            print(self.test_freezer_obj.freezer.returning_clause)
            with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBU_model:
                mock_PBU_model.get.return_value = PlatiniumBotUser(
                    bot_user_id=1,
                    user_telegram_id=self.tlg_user_id,
                    bot_user_name=self.tlg_username,
                    bot_user_phone=self.tlg_phone,
                    bot_user_active=True,
                    bot_user_joined_timestamp=datetime.datetime.now(
                        tz=timezone.utc
                        )
                    )

                mock_PBU_model.user_telegram_id = self.tlg_user_id

                mock_PBU_model.save.return_value = 1

                updated_user = self.test_freezer_obj.update_bot_user(
                    active_status=self.tlg_active_status,
                    telegram_id=self.tlg_user_id
                )

                mock_PBU_model.save.assert_called()
                self.assertFalse(updated_user.bot_user_active)
    """

    def test_get_bot_user(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBU_model:
                mock_PBU_model.get.return_value = PlatiniumBotUser(
                    bot_user_id=1,
                    user_telegram_id=self.tlg_user_id,
                    bot_user_name=self.tlg_username,
                    bot_user_phone=self.tlg_phone,
                    bot_user_active=True,
                    bot_user_joined_timestamp=datetime.datetime.now(
                        tz=timezone.utc
                    )
                )
                mock_PBU_model.user_telegram_id = self.tlg_user_id

                user = self.test_freezer_obj.get_bot_user(self.tlg_user_id)

                mock_PBU_model.get.assert_called_with(
                    mock_PBU_model.user_telegram_id == self.tlg_user_id
                )
                self.assertEqual(user.user_telegram_id, self.tlg_user_id)
                self.assertEqual(user.bot_user_name, self.tlg_username)

    def test_add_new_content(self):
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            with patch("src.freezer.PlatiniumBotContent") as mock_PBC_model:
                content_list = {
                    'time': '17:55',
                    'teams': 'Slavia Prague - Rangers',
                    'odds': '1.38',
                    'country': 'euro.L',
                    '3ways': 'over 1.5'
                }
                self.test_freezer_obj.add_new_content(
                    content_list['time'],
                    content_list['teams'],
                    content_list['odds'],
                    content_list['country'],
                    content_list['3ways']
                )
                # mock_PBC_model.create.assert_called()
                mock_PBC_model.create.assert_called_with(
                    platinium_content_time=content_list['time'],
                    platinium_content_teams=content_list['teams'],
                    platinium_content_odds=content_list['odds'],
                    platinium_content_country=content_list['country'],
                    platinium_content_3ways=content_list['3ways']
                )

    def test_get_today_bot_content(self):
        """
        todo:
            test if it returns today's matches
            test if it returns the matches in a list of dicts
        test_get_bot_content [summary]
        """
        with patch("peewee.MySQLDatabase", autospec=True) as mock_db:
            self.test_freezer_obj = Freezer()
            with patch("src.freezer.PlatiniumBotUser", autospec=True) as mock_PBC_model:
                mock_PBC_model.select.return_value = PlatiniumBotContent(
                    platinium_content_time='17:55',
                    platinium_content_teams='Slavia Prague - Rangers',
                    platinium_content_odds='1.38',
                    platinium_content_country='euro.L',
                    platinium_content_3ways='over 1.5',
                    # platinium_content_result=peewee.TextField(default=""),
                    platinium_content_posted_timestamp=datetime.datetime.today()
                )
                content = self.test_freezer_obj.get_today_bot_content()

                self.assertIsInstance(content, peewee.ModelSelect)
                self.assertIsInstance(content.platinium_content_time, str)

                mock_PBC_model.select.assert_called()
                mock_PBC_model.where.assert_called()

                # self.assertIsInstance(content, list)
                # self.assertGreater(len(content), 0)
                # content_dict = content.pop(0)
                # self.assertIsInstance(content_dict, dict)
                # self.assertIn("teams", content_dict)


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
