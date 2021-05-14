import logging
import configparser

from telethon import (
    TelegramClient,
    errors,
    events,
    Button
    )

from cooker import (Cooker)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} PlatiniumBot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)

url_dict = {
    0: "https://xxviptips.blogspot.com/",
    1: "https://hsitoriiquebet.blogspot.com/",
    2: "https://xxgoldtips.blogspot.com/",
    3: "https://xxcombotips.blogspot.com/"
}

config = configparser.ConfigParser()
config.read('data/.conbt.ini')

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
bot_token = config['Telegram']['bot_token']

bot = TelegramClient('platinium', api_id, api_hash).start(bot_token=bot_token)


@bot.on(events.NewMessage(pattern="/start"))
async def send_msg_when_start(event):
    ngx = await bot.get_entity('@Negassa_B')
    if event.sender_id != ngx.id:
        await event.respond("you are not allowed to use this bot, good bye")
    else:
        cooker = Cooker(url_dict[0])
        cooker.get_sauce()  # perhaps change this to await
        tables = cooker.cook_sauce()
        one_table = tables.pop()
        await event.respond(one_table, parse_mode='HTML')

with bot:
    bot.run_until_disconnected()
