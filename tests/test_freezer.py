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
# from tests.do_something import add_user_for_testing


class FreezerTestSuites(unittest.TestCase):
    """
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
        self.test_freezer_obj = Freezer(True)
        self.test_freezer_obj.open_freezer()

    def tearDown(self):
        self.test_freezer_obj.testing = False
        self.test_freezer_obj.close_freezer()
        self.test_freezer_obj = None

    def test_create_bot_tables(self):
        try:
            self.test_freezer_obj.create_bot_tables()
        except Exception as e:
            print(f"test failed due to exception {e}")
        else:
            self.assertTrue(self.test_freezer_obj.freezer.table_exists("table_PlatiniumBotUser"))
            self.assertTrue(self.test_freezer_obj.freezer.table_exists("table_PlatiniumBotContent"))

    def test_add_new_bot_user(self):
        self.test_freezer_obj = Freezer(testing=True)
        add_user_for_testing(
            freezer_obj=self.test_freezer_obj,
            tg_user_id=self.tlg_user_id,
            tg_phone=self.tlg_phone,
            tg_username=self.tlg_username,
            tg_first_name=self.tlg_first_name
        )
        val = PlatiniumBotUser.get(PlatiniumBotUser.user_telegram_id == self.tlg_user_id)
        self.assertEqual(val.user_telegram_id, self.tlg_user_id)

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
        add_user_for_testing(
            freezer_obj=self.test_freezer_obj,
            tg_user_id=self.tlg_user_id,
            tg_phone=self.tlg_phone,
            tg_username=self.tlg_username,
            tg_first_name=self.tlg_first_name
        )
        user = self.test_freezer_obj.get_bot_user(self.tlg_user_id)
        if user is not None:
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
            with patch("src.freezer.PlatiniumBotContent", autospec=True) as mock_PBC_model:
                mock_PBC_model.select().where().return_value = list(
                    peewee.ModelSelect(
                        model=PlatiniumBotContent,
                        fields_or_models=[
                            PlatiniumBotContent(
                                platinium_content_time='17:55',
                                platinium_content_teams='Slavia Prague - Rangers',
                                platinium_content_odds='1.38',
                                platinium_content_country='euro.L',
                                platinium_content_3ways='over 1.5',
                                platinium_content_posted_timestamp=datetime.datetime.today()
                            ),
                            PlatiniumBotContent(
                                platinium_content_time='17:55',
                                platinium_content_teams='Slavia Prague - Rangers',
                                platinium_content_odds='1.38',
                                platinium_content_country='euro.L',
                                platinium_content_3ways='over 1.5',
                                platinium_content_posted_timestamp=datetime.datetime.today()
                            ),
                            PlatiniumBotContent(
                                platinium_content_time='17:55',
                                platinium_content_teams='Slavia Prague - Rangers',
                                platinium_content_odds='1.38',
                                platinium_content_country='euro.L',
                                platinium_content_3ways='over 1.5',
                                platinium_content_posted_timestamp=datetime.datetime.today()
                            )
                        ]
                    ).dicts()
                )
                content = self.test_freezer_obj.get_today_bot_content()

                self.assertIsInstance(content, list)
                self.assertGreater(len(content), 0)
                val1 = content.pop(0)
                self.assertIsInstance(val1, dict)
                self.assertIn("platinium_content_time", val1.keys())
                self.assertIn("17:55", val1.values())

                mock_PBC_model.select.assert_called()
                mock_PBC_model.where.assert_called()


def add_user_for_testing(freezer_obj, tg_user_id, tg_phone, tg_username, tg_first_name):
    freezer_obj.create_bot_tables()
    if tg_username is None and tg_phone is None:
        freezer_obj.add_new_bot_user(
            tg_user_id,
            tg_first_name
        )

        print("both username & phone ARE NONE")
    elif tg_username is None and tg_phone is not None:
        freezer_obj.create_new_bot_user(
            telegram_id=tg_user_id,
            telegram_name=tg_first_name,
            phone=tg_phone
        )

        print("phone NOT NONE")
    elif tg_phone is None and tg_username is not None:
        freezer_obj.create_new_bot_user(
            telegram_id=tg_user_id,
            telegram_name=tg_username
        )

        print("username NOT NONE")
    else:
        freezer_obj.add_new_bot_user(
            telegram_id=tg_user_id,
            telegram_name=tg_username,
            phone=tg_phone
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
