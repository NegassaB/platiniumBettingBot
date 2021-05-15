import logging
import configparser

from telethon import (
    TelegramClient,
    errors,
    events,
    Button
    )

from cooker import (Cooker)
from freezer import Freezer

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
    3: "https://xxcombotips.blogspot.com/"  # fix: won't work, avoid using till fixed
}

config = configparser.ConfigParser()
config.read('data/.conbt.ini')

bot_api_id = config['Telegram']['bot_api_id']
bot_api_hash = config['Telegram']['bot_api_hash']
bot_token = config['Telegram']['bot_token']
platinium_channel_id = config['Telegram']['platinium_channel_id']

bot = TelegramClient(
    'platinium',
    bot_api_id,
    bot_api_hash
).start(bot_token=bot_token)


async def main():
    platinium_channel = await bot.get_entity(int(platinium_channel_id))
    vip_cook = Cooker(url_dict[0])
    total_matches = vip_cook.cook_sauce()
    # bot.parse_mode = "md"
    for match in total_matches:
        # todo: find a remove characters like \u \xa0
        # todo: build the markdown table here and finally send it
        await bot.send_message(platinium_channel, str(match))
    # await bot.send_message(platinium_channel, "what is up nigggaaar")


def get_today_viptips():
    vip_cook = Cooker(url_dict[0])
    res = vip_cook.cook_recipe()


async def post_today_viptips():
    pass


@bot.on(events.NewMessage)
async def send_msg_when_start(event):
    if event.sender_id != 355355326:
        await event.respond(
            "you are not allowed to use this bot, please checkout the group instead good bye"
        )
    gadd = await bot.get_entity(event.sender_id)
    await bot.send_message(gadd, "what Gadd?")
    # cooker = Cooker(url_dict[0])
    # cooker.get_sauce()  # perhaps change this to await
    # tables = cooker.cook_sauce()
    # one_table = tables.pop()
    # await event.respond(one_table, parse_mode='HTML')

with bot:
    bot.loop.run_until_complete(main())
    # bot.run_until_disconnected()
