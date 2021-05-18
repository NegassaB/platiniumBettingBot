import logging
import configparser

from telethon import (
    TelegramClient,
    events,
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
    3: "https://xxcombotips.blogspot.com/"  # fix: site has a different format, won't work, avoid using till fixed
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

bot.parse_mode = "md"

"""
todo:
        [ ] - run post_today_tips everyday @ 5:00
        [ ] - run post_today_results everyday @ 3:00
        [x] - store the message id so as to reply to that when results are posted
"""


async def main():
    platinium_channel = await bot.get_entity(int(platinium_channel_id))
    await post_today_viptips(platinium_channel)
    await post_yesterday_results(platinium_channel)


def get_today_viptips():
    vip_cook = Cooker(url_dict[0])
    total_matches = vip_cook.cook_sauce()

    return extract_and_generate_markdown_match_table(total_matches)


def get_viptips_results():
    viptips_result_cook = Cooker(url_dict[1])
    total_matches = viptips_result_cook.cook_sauce()

    return extract_and_generate_markdown_match_table(total_matches)


def extract_and_generate_markdown_match_table(total_matches):
    match_table = "**| League & Time | Match | Threeway | Odds | Rating | Final result |**"
    separator = "".join(["-"] * 85)
    match_table = "".join([match_table, "\n", separator])
    for match in total_matches:
        match_table = "".join([match_table, "\n", "```", str(match), ", ", "```\n"])
    return match_table


async def post_today_viptips(platinium_channel):
    global last_posted_id

    # fix: run in a different thread or coroutine (I don't think this doable cause it uses requests)
    matches_table = get_today_viptips()

    await bot.unpin_message(platinium_channel)

    msg_viptips_posted = await bot.send_message(platinium_channel, matches_table)
    await bot.pin_message(platinium_channel, msg_viptips_posted, notify=True)

    last_posted_id = msg_viptips_posted.id


async def post_yesterday_results(platinium_channel):
    # fix: run in a different thread or coroutine (I don't think this doable cause it uses requests)
    matches_table = get_viptips_results()

    await bot.unpin_message(platinium_channel)

    msg_results_posted = await bot.send_message(platinium_channel, matches_table, reply_to=last_posted_id)

    await bot.pin_message(platinium_channel, msg_results_posted, notify=True)


@bot.on(events.NewMessage)
async def send_msg_when_start(event):
    if event.sender_id != 355355326:
        msg = "you are not allowed to use this bot,\
            please checkout the group https://t.me/joinchat/SkEhcPc2yx_Wmh7S instead. Good bye."
        await event.respond(msg)
    gadd = await bot.get_entity(event.sender_id)
    await bot.send_message(gadd, "what Gadd?")

with bot:
    bot.loop.run_until_complete(main())
    # bot.run_until_disconnected()
