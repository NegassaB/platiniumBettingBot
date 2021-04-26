import unittest
import datetime
import dateutil.parser
from unittest.mock import (MagicMock, patch)

from src.freezer import (
    peewee,
    Freezer,
    BaseFarm,
    PlatiniumBotUser
)


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

    def test_add_new_bot_user(self):
        add_user_for_testing(self.test_freezer_obj)
        val = PlatiniumBotUser.get(PlatiniumBotUser.user_telegram_id == self.tlg_user_id)
        self.assertEqual(val.user_telegram_id, self.tlg_user_id)

    def test_get_bot_user(self):
        add_user_for_testing(self.test_freezer_obj)
        user = self.test_freezer_obj.get_bot_user(self.tlg_user_id)
        if user is not None:
            self.assertEqual(user.user_telegram_id, self.tlg_user_id)
            self.assertEqual(user.bot_user_name, self.tlg_username)

    def test_delete_bot_user(self):
        add_user_for_testing(self.test_freezer_obj)
        user_2_check = self.test_freezer_obj.get_bot_user(self.tlg_user_id)
        self.test_freezer_obj.delete_bot_user(False, self.tlg_user_id)
        user_after_deletion = self.test_freezer_obj.get_bot_user(self.tlg_user_id)
        self.assertFalse(user_after_deletion.bot_user_active)
        self.assertNotEqual(
            user_2_check.bot_user_active,
            user_after_deletion.bot_user_active
        )


def add_user_for_testing(freezer_obj):
    tg_user_id = 355355326
    # tg_username = None
    tg_username = "Gadd"
    tg_first_name = "Negassa"
    # tg_phone = None
    tg_phone = "+251911985365"
    tlg_active_status = False

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

    def test_models_instance_basemodel(self):
        self.assertIsInstance(self.platinium_bot_user, BaseFarm)
        self.assertIsInstance(self.platinium_bot_user, peewee.Model)
