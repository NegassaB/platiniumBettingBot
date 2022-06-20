import logging
import configparser
import time
import datetime

import pytz
from telethon import (
    TelegramClient,
    events,
    errors
)

from cooker import (Cooker)
from freezer import Freezer

# enable logging
logging.basicConfig(
    filename=f"log {__name__} PlatiniumBot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)

url_dict = {
    0: "https://dailyviptipsx.blogspot.com/",
    1: "https://statistiquesxx.blogspot.com/",
    2: "https://xxgoldtips.blogspot.com/?m=0",
    3: "https://xxcombotips.blogspot.com/?m=0"
}

config = configparser.ConfigParser()
config.read('data/.conbt.ini')

BOT_API_ID = config['Telegram']['bot_api_id']
BOT_API_HASH = config['Telegram']['bot_api_hash']
BOT_TOKEN = config['Telegram']['bot_token']
CHANNEL_ID = config['Telegram']['channel_id']
ADMIN_ID = config['Telegram']['admin_id']

try:
    bot = TelegramClient(
        'platinium',
        BOT_API_ID,
        BOT_API_HASH
    ).start(bot_token=BOT_TOKEN)
except Exception as e:
    logger.exception(str(e), exc_info=True)
else:
    bot.parse_mode = "md"
    AA_TIMEZONE = pytz.timezone('Africa/Addis_Ababa')
    queue_id = []
    queue_id.append(708)

"""
todo:
        [ ] - retrieve and store users' telegram ids
        [ ] - build the combo & golden tips provider using commands instead of posting on channel
"""


async def main():

    async def recall_main():
        logger.info("restarting main")
        await main()

    try:
        # platinium_channel = await bot.get_entity(int(platinium_channel_id))
        platinium_channel = await bot.get_input_entity("https://t.me/platiniumbettingtips")
    except errors.FloodWaitError as fwe:
        logger.error(f"hit the FloodWaitError, got sleep for {fwe.seconds} seconds")
        time.sleep(fwe.seconds)
    except errors.FloodError as fe:
        logger.error(f"hit the FloodError with message -- {fe.message}")
        time.sleep(5000)
    except Exception as e:
        logger.exception(f"hit exception -- {e}")
        await recall_main()
    else:
        await post_yesterday_results(platinium_channel)
        logger.info("sleeping after post_yesterday_results")
        time.sleep(3600)
        await post_today_viptips(platinium_channel)


def get_tips_or_results(result_tips=None):
    cooker = None
    if result_tips == "viptips":
        cooker = Cooker(url_dict[0])
    elif result_tips == "goldtips":
        cooker = Cooker(url_dict[2])
    else:
        cooker = Cooker(url_dict[1])
    total_matches = cooker.cook_sauce()

    return extract_and_generate_markdown_match_table(total_matches)


def extract_and_generate_markdown_match_table(total_matches):
    match_table = "**| League & Time | Match | Threeway | Odds | Rating | Final result |**"
    separator = "".join(["-"] * 70)
    match_table = "".join([match_table, "\n", separator])
    for match in total_matches:
        match_table = "".join([match_table, "\n", "```", str(match), ", ", "```\n"])
    return match_table


async def post_today_viptips(platinium_channel):
    logger.info("starting post_today_viptips")

    # fixme: run in a different thread or coroutine (I don't think this doable cause it uses requests)
    matches_table = get_tips_or_results("viptips")

    await bot.unpin_message(platinium_channel)

    warning_msg = "".join(
        [
            "Dear followers, be smart and don't bet the entire tips in one ticket. ",
            "Instead break them down in to 3 or 4 tickets."
        ]
    )

    await bot.send_message(platinium_channel, warning_msg)
    time.sleep(2)
    msg_viptips_posted = await bot.send_message(platinium_channel, matches_table)
    await bot.pin_message(platinium_channel, msg_viptips_posted, notify=True)

    queue_id.append(msg_viptips_posted.id)

    logger.info("finished with post_today_viptips")


async def post_yesterday_results(platinium_channel):
    logger.info("starting post_yesterday_results")
    # fixme: run in a different thread or coroutine (I don't think this doable cause it uses requests)
    matches_table = get_tips_or_results()

    await bot.unpin_message(platinium_channel)

    if len(queue_id) == 0:
        msg_results_posted = await bot.send_message(platinium_channel, matches_table)
    else:
        msg_results_posted = await bot.send_message(platinium_channel, matches_table, reply_to=queue_id.pop(0))

    await bot.pin_message(platinium_channel, msg_results_posted, notify=True)

    time.sleep(2)

    warning_msg = "".join(
        [
            "This application is only an informative tool and must be used just for fun.\n",
            "We post various sports analysis that represent our provider's opinion regarding\t",
            "the eventual outcome of those games."
        ]
    )

    await bot.send_message(platinium_channel, warning_msg)

    logger.info("finished with post_yesterday_results")


def time_check(right_now):
    if right_now.time() >= datetime.time(
        hour=14, minute=0, tzinfo=AA_TIMEZONE) and right_now.time() <= datetime.time(
            hour=14, minute=2, tzinfo=AA_TIMEZONE):
        return True
    else:
        return False


@bot.on(events.NewMessage)
async def send_msg_when_start(event):
    if event.sender_id != ADMIN_ID:
        msg = "you are not allowed to use this bot,\
            please checkout the group https://t.me/joinchat/SkEhcPc2yx_Wmh7S instead. Good bye."
        await event.respond(msg)
    gadd = await bot.get_entity(event.sender_id)
    await bot.send_message(gadd, "what Gadd?")

with bot:
    while 1:
        right_now = datetime.datetime.now(tz=AA_TIMEZONE)
        if time_check(right_now):
            bot.loop.run_until_complete(main())
        time.sleep(60)
        # bot.loop.run_until_complete(main())
        logger.info(f"{right_now} -- looping")
