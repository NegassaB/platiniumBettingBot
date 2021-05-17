import logging
import configparser

from telethon import (
    TelegramClient,
    errors,
    events,
    Button
    )

import markdown_strings

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

"""
todo:
        [ ] - run post_today_tips everyday @ 5:00
        [ ] - run post_today_results everyday @ 3:00
"""


async def main():
    platinium_channel = await bot.get_entity(int(platinium_channel_id))
    matches_table = get_today_viptips()
    bot.parse_mode = "md"
    await bot.send_message(platinium_channel, matches_table)
    # await bot.send_message(platinium_channel, "what is up nigggaaar")


def get_today_viptips():
    vip_cook = Cooker(url_dict[0])
    total_matches = vip_cook.cook_sauce()

    match_table = "**League & Time | Match | Threeway | Odds | Rating | Final result**"
    separator = "".join(["-"] * 105)
    match_table = "".join([match_table, "\n", separator])

    for match in total_matches:
        match_table = "".join([match_table, "\n", "```", str(match), ", ", "```"])

    return match_table


async def post_today_viptips():
    pass


@bot.on(events.NewMessage)
async def send_msg_when_start(event):
    if event.sender_id != 355355326:
        msg = "you are not allowed to use this bot,\
            please checkout the group https://t.me/joinchat/SkEhcPc2yx_Wmh7S instead good bye"
        await event.respond(msg)
    gadd = await bot.get_entity(event.sender_id)
    await bot.send_message(gadd, "what Gadd?")

with bot:
    bot.loop.run_until_complete(main())
    # bot.run_until_disconnected()
