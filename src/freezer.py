import logging
from datetime import (datetime, timezone)

# 3rd party libraries
import peewee


log_fmt = "%(asctime)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s"
# enable logging
logging.basicConfig(
    format=log_fmt,
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

database_proxy = peewee.DatabaseProxy()


class Freezer():
    """
    todo:   [x]. update add_new_user() according to the new details
            [x]. update get_bot_user() according to the new details
            [x]. rename update_bot_user() to delete_bot_user(), actions are similar

    Freezer [summary]

    Returns:
        [type]: [description]
    """
    db_name = "platinium_bot_db"
    db_username = "platinium_bot"
    db_pswd = "platinium_pswd"

    def __init__(self, testing=False):
        """
        __init__ [summary]
        """
        if testing:
            self.freezer = peewee.SqliteDatabase(":memory:", autoconnect=False)
            self.testing = True
        else:
            self.freezer = peewee.MySQLDatabase(
                database=Freezer.db_name,
                user=Freezer.db_username,
                password=Freezer.db_pswd,
                host="localhost",
                port=3306,
                autoconnect=False
            )
            self.testing = False
        database_proxy.initialize(self.freezer)

    def open_freezer(self):
        """
        open_freezer [summary]

        Returns:
            [type]: [description]
        """
        if self.freezer.is_closed():
            self.freezer.connect(reuse_if_open=True)
            print('\nconnected to db\n')

    def close_freezer(self):
        """
        close_freezer [summary]

        Returns:
            [type]: [description]
        """
        if self.testing and not self.freezer.is_closed():
            print("\n not closing cxn to db cause you're testing :)\n")
            pass
        elif not self.freezer.is_closed():
            self.freezer.close()
            print('\nclosed cxn to db\n')
        else:
            print('\n dont know what to put in the else block of close_freezer()\n')

    def create_bot_tables(self):
        """
        create_bot_tables: checks for existence and if they don't exist, creates the database
                        tables that the bot uses.
        """
        if self.freezer.is_closed():
            self.open_freezer()
        tbl_list = []
        if not self.freezer.table_exists("table_PlatiniumBotUser"):
            tbl_list.append(PlatiniumBotUser)

        if len(tbl_list) != 0:
            try:
                self.freezer.create_tables(models=tbl_list)
            except peewee.PeeweeException as pex:
                logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
                raise pex
            except Exception as e:
                logger.exception(f"exception occurred -- {e}", exc_info=True)
                raise e
            finally:
                self.close_freezer()

    def add_new_bot_user(self, telegram_id, telegram_name, phone=None):
        """
        add_new_bot_user [summary]

        Args:
            telegram_id ([type]): [description]
            telegram_name ([type]): [description]
        """
        if self.freezer.is_closed():
            self.open_freezer()
        try:
            if phone is not None:
                PlatiniumBotUser.create(
                    user_telegram_id=telegram_id,
                    bot_user_name=telegram_name,
                    bot_user_phone=phone
                )
            else:
                PlatiniumBotUser.create(
                    user_telegram_id=telegram_id,
                    bot_user_name=telegram_name
                )
        except peewee.PeeweeException as pex:
            logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
        except Exception as e:
            logger.exception(f"Exception occurred -- {e}", exc_info=True)
        finally:
            self.close_freezer()

    def get_bot_user(self, telegram_id):
        """
        get_bot_user [summary]

        Args:
            telegram_id (int): the telegram id of the user that is required.

        Returns:
            PlatiniumBotUser: an instance of PlatiniumBotUser that contains the required data.
        """
        if self.freezer.is_closed():
            self.open_freezer()
        try:
            result = PlatiniumBotUser.get(PlatiniumBotUser.user_telegram_id == telegram_id)
            return result
        except peewee.PeeweeException as pex:
            logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
        except Exception as e:
            logger.exception(f"Exception occurred -- {e}", exc_info=True)
        finally:
            self.close_freezer()

    def delete_bot_user(self, active_status, telegram_id):
        """
        delete_bot_user [summary]

        Args:
            active_status ([type]): [description]
            telegram_id ([type]): [description]

        Returns:
            [type]: [description]
        """
        user_2_update = self.get_bot_user(telegram_id)
        if self.freezer.is_closed():
            self.open_freezer()
        try:
            user_2_update.bot_user_active = active_status
            user_2_update.save()
        except peewee.PeeweeException as pex:
            logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
        except Exception as e:
            logger.exception(f"Exception occurred -- {e}", exc_info=True)
        finally:
            self.close_freezer()


class BaseFarm(peewee.Model):
    """
    BaseModel [summary]

    Args:
        peewee.Model ([type]): [description]
    """
    class Meta():
        database = database_proxy


class PlatiniumBotUser(BaseFarm):
    bot_user_id = peewee.AutoField(primary_key=True, null=False)
    user_telegram_id = peewee.IntegerField(null=False, unique=True)
    bot_user_name = peewee.CharField(max_length=255)
    bot_user_phone = peewee.CharField(
        max_length=20,
        default="00000000000000"
    )

    # todo: set this to in-active if the user stops & deletes the bot
    bot_user_active = peewee.BooleanField(default=True, null=False)
    bot_user_joined_timestamp = peewee.DateTimeField(
        null=False,
        default=datetime.now(tz=timezone.utc)
    )

    class Meta():
        table_name = "table_PlatiniumBotUser"
