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
    todo:
        [ ]. build add_new_content()
            in this find a way to to get the actual message instead of the fk
        [ ]. build add_new_message()
        []. build a way to update platinium_content_posted_timestamp after posting
        [ ]. build the CRUD operation methods

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
        if not self.freezer.table_exists("table_PlatiniumBotContent"):
            tbl_list.append(PlatiniumBotContent)

        if (tbl_list) != 0:
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

    def update_bot_user(self, active_status, telegram_id):
        """
        todo: build the update_bot_user code & test it
        update_bot_user [summary]

        Args:
            active_status ([type]): [description]
            telegram_id ([type]): [description]

        Returns:
            [type]: [description]
        """
       pass

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

    def add_new_content(self, content_time, content_teams, content_odds, content_country, content_3ways):
        """
        add_new_content [summary]

        Args:
            content_time ([type]): [description]
            content_teams ([type]): [description]
            content_odds ([type]): [description]
            content_country ([type]): [description]
            content_3ways ([type]): [description]
        """
        if not self.db_open:
            self.open_freezer()
        try:
            PlatiniumBotContent.create(
                platinium_content_time=content_time,
                platinium_content_teams=content_teams,
                platinium_content_odds=content_odds,
                platinium_content_country=content_country,
                platinium_content_3ways=content_3ways
            )
        except peewee.PeeweeException as pex:
            logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
        except Exception as e:
            logger.exception(f"Exception occurred -- {e}", exc_info=True)
        finally:
            self.close_freezer()

    def get_today_bot_content(self):
        """
        todo:
            make it return a list of dicts today's matches
        get_bot_content [summary]
        """
        if not self.db_open:
            self.open_freezer()
        try:
            return list(PlatiniumBotContent.select().where(
                PlatiniumBotContent.platinium_content_posted_timestamp == datetime.today()
            ).dicts()
            )
            # return PlatiniumBotContent.select().where(
            #     PlatiniumBotContent.platinium_content_posted_timestamp == datetime.today().date()
            # )
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

    bot_user_active = peewee.BooleanField(default=True, null=False)
    bot_user_joined_timestamp = peewee.DateTimeField(
        null=False,
        default=datetime.now(tz=timezone.utc)
    )

    class Meta():
        table_name = "table_PlatiniumBotUser"


class PlatiniumBotContent(BaseFarm):
    platinium_content_id = peewee.AutoField(primary_key=True, null=False)
    platinium_content_time = peewee.CharField(10)
    platinium_content_teams = peewee.TextField()
    platinium_content_odds = peewee.CharField(10)
    platinium_content_country = peewee.CharField(30)
    platinium_content_3ways = peewee.CharField(25)
    # todo update this when results b/me available after you scrape it
    platinium_content_result = peewee.TextField(default="")

    # todo update this when the content is posted
    platinium_content_posted_timestamp = peewee.DateTimeField(
        null=False,
        default=datetime.now(tz=timezone.utc),
    )

    class Meta():
        table_name = "table_PlatiniumBotContent"
