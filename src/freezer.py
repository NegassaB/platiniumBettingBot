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
        # mock_db.return_value.connect = peewee.MySQLDatabase.connect()
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
            print('\nconnected\n')

    def close_freezer(self):
        """
        close_freezer [summary]

        Returns:
            [type]: [description]
        """
        if not self.freezer.is_closed():
            self.freezer.close()

    def create_table(self):
        pass


class BaseModel(peewee.Model):

    class Meta():
        database = Freezer()


class PlatiniumBotUser(BaseModel):
    bot_user_id = peewee.AutoField(primary_key=True, null=False)
    user_telegram_id = peewee.IntegerField(null=False, unique=True)
    bot_user_name = peewee.CharField(max_length=255)

    bot_user_joined_timestamp = peewee.DateTimeField(null=False, default=datetime.now(tz=timezone.utc))
    bot_user_active = peewee.BooleanField(default=False, null=False)
