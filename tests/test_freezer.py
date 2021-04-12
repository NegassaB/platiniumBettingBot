import unittest
import datetime
import dateutil.parser
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
        self.test_freezer_obj.create_bot_tables()

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
        add_user_for_testing(
            freezer_obj=self.test_freezer_obj,
            tg_user_id=self.tlg_user_id,
            tg_phone=self.tlg_phone,
            tg_username=self.tlg_username,
            tg_first_name=self.tlg_first_name
        )
        val = PlatiniumBotUser.get(PlatiniumBotUser.user_telegram_id == self.tlg_user_id)
        self.assertEqual(val.user_telegram_id, self.tlg_user_id)

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

    def test_update_bot_user(self):
        add_user_for_testing(
            freezer_obj=self.test_freezer_obj,
            tg_user_id=self.tlg_user_id,
            tg_phone=self.tlg_phone,
            tg_username=self.tlg_username,
            tg_first_name=self.tlg_first_name
        )

        self.test_freezer_obj.update_bot_user(
            active_status=self.tlg_active_status,
            telegram_id=self.tlg_user_id
        )

        user = self.test_freezer_obj.get_bot_user(self.tlg_user_id)
        self.assertFalse(user.bot_user_active)

    def test_add_new_content(self):
        add_content_for_testing(self.test_freezer_obj)
        val = PlatiniumBotContent.get(
            PlatiniumBotContent.platinium_content_teams == 'Slavia Prague - Rangers'
        )
        self.assertEqual(val.platinium_content_country, 'euro.L')

    def test_get_bot_content_today(self):
        """
        test_get_bot_content [summary]
        """
        add_content_for_testing(self.test_freezer_obj)
        content = self.test_freezer_obj.get_bot_content_today()
        self.assertIsInstance(content, list)
        self.assertGreater(len(content), 0)
        val1 = content.pop(0)
        self.assertIsInstance(val1, dict)
        self.assertIn("platinium_content_time", val1.keys())
        self.assertIn("over 1.5", val1.values())
        val_posted_date = dateutil.parser.parse(
            val1["platinium_content_posted_timestamp"]
        )
        self.assertEqual(val_posted_date.date(), datetime.datetime.today().date())

    def test_update_bot_content(self):
        pass


def add_user_for_testing(freezer_obj, tg_user_id, tg_phone, tg_username, tg_first_name):
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


def add_content_for_testing(freezer_obj):
    content_list = {
        'time': '17:55',
        'teams': 'Slavia Prague - Rangers',
        'odds': '1.38',
        'country': 'euro.L',
        '3ways': 'over 1.5'
    }
    x = 5
    while x != 0:
        x -= 1
        freezer_obj.add_new_content(
            content_list['time'],
            content_list['teams'],
            content_list['odds'],
            content_list['country'],
            content_list['3ways']
        )


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
