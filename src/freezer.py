import logging
from datetime import (datetime, timezone)

# 3rd party libraries
import peewee


log_fmt = "%(asctime)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s"
# enable logging
logging.basicConfig(
    format=log_fmt,
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class Freezer():
    """
    todo:
        []. build create_table()
            condn is: if tables don't exist, create the necessary tables in create_table()
            if it does exist, skip
        []. build the CRUD operation methods
    Freezer [summary]

    Returns:
        [type]: [description]
    """
    db_name = "platinium_bot_db"
    db_username = "platinium_bot"
    db_pswd = "platinium_pswd"

    def __init__(self):
        """
        __init__ [summary]
        """
        self.freezer = peewee.MySQLDatabase(
            database=Freezer.db_name,
            user=Freezer.db_username,
            password=Freezer.db_pswd,
            host="localhost",
            port=3306
        )

    def open_freezer(self):
        """
        open_freezer [summary]

        Returns:
            [type]: [description]
        """
        if self.freezer.connect():
            print('\nconnected to db\n')

    def close_freezer(self):
        """
        close_freezer [summary]

        Returns:
            [type]: [description]
        """
        # if not self.freezer.close():
        if self.freezer.close():
            print('\nclosed cxn to db\n')

    def create_table(self):
        pass


class BaseModel(peewee.Model):
    """
    todo:
        [ ] - override update() PlatiniumMessage to update platinium_content_result when data b/mes available
    hack[ ] - for the above perhaps might be to override something in the PlatiniumBotContent to return the full
                content instead of the id number
    BaseModel [summary]

    Args:
        peewee.Model ([type]): [description]
    """
    class Meta():
        database = Freezer()


class PlatiniumBotUser(BaseModel):
    bot_user_id = peewee.AutoField(primary_key=True, null=False)
    user_telegram_id = peewee.IntegerField(null=False, unique=True)
    bot_user_name = peewee.CharField(max_length=255)

    bot_user_active = peewee.BooleanField(default=False, null=False)
    bot_user_joined_timestamp = peewee.DateTimeField(
        null=False,
        default=datetime.now(tz=timezone.utc)
    )


class PlatiniumBotContent(BaseModel):
    platinium_content_id = peewee.AutoField(primary_key=True, null=False)
    platinium_content_time = peewee.CharField(50)
    platinium_content_odds = peewee.CharField(10)
    platinium_content_country = peewee.CharField(25)
    platinium_content_3ways = peewee.CharField(15)
    platinium_content_result = peewee.CharField(max_length=15)

    platinium_content_timestamp = peewee.DateTimeField(
        null=False,
        default=datetime.now(tz=timezone.utc)
    )


class PlatiniumMessage(BaseModel):
    platinium_msg_id = peewee.AutoField(primary_key=True, null=False)
    platinium_msg_content = peewee.ForeignKeyField(
        PlatiniumBotContent,
        null=False,
        related_name="fk_platinium_content",
        on_update='cascade',
        on_delete='restrict'
    )
    platinium_msg_user = peewee.ForeignKeyField(
        PlatiniumBotUser,
        null=False,
        related_name='fk_platinium_bot_user',
        on_update='cascade',
        on_delete='restrict'
    )

    platinium_msg_sent_timestamp = peewee.DateTimeField(
        null=False,
        default=datetime.now(tz=timezone.utc)
    )
