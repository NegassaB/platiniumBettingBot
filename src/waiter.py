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
    3: "https://xxcombotips.blogspot.com/"  # fixme: site has a different format, won't work, avoid using till fixed
}

config = configparser.ConfigParser()
config.read('data/.conbt.ini')

bot_api_id = config['Telegram']['bot_api_id']
bot_api_hash = config['Telegram']['bot_api_hash']
bot_token = config['Telegram']['bot_token']
platinium_channel_id = config['Telegram']['platinium_channel_id']

try:
    bot = TelegramClient(
        'platinium',
        bot_api_id,
        bot_api_hash
    ).start(bot_token=bot_token)
except Exception as e:
    logger.exception(str(e), exc_info=True)
else:
    bot.parse_mode = "md"
    AA_TIMEZONE = pytz.timezone('Africa/Addis_Ababa')
    vipttips_posted = False

"""
todo:   [x] - run post_today_tips everyday @ 5:00
        [x] - run post_today_results everyday @ 3:00
        [x] - store the message id so as to reply to that when results are posted
"""


async def main():

    async def recall_main():
        logger.info("restarting main")
        await main()

    try:
        platinium_channel = await bot.get_entity(int(platinium_channel_id))
    except errors.FloodWaitError as fwe:
        logger.error(f"hit the FloodWaitError, got sleep for {fwe.seconds} seconds")
        time.sleep(fwe.seconds)
    except errors.FloodError as fe:
        logger.error(f"hit the FloodError with message -- {e.message}")
        time.sleep(5000)
    except Exception as e:
        logger.exception(f"hit exception -- {e}")
        await recall_main()
    else:
        if not vipttips_posted:
            await post_today_viptips(platinium_channel)
        elif vipttips_posted:
            await post_yesterday_results(platinium_channel)
        else:
            logger.info(f"viptips_posted is {viptips_posted}, IDK how I got here")


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
    logger.info("starting post_today_viptips")
    global last_posted_id
    global vipttips_posted

    # fixme: run in a different thread or coroutine (I don't think this doable cause it uses requests)
    matches_table = get_today_viptips()

    await bot.unpin_message(platinium_channel)

    msg_viptips_posted = await bot.send_message(platinium_channel, matches_table)
    await bot.pin_message(platinium_channel, msg_viptips_posted, notify=True)

    last_posted_id = msg_viptips_posted.id

    vipttips_posted = True

    logger.info("finished with post_today_viptips")


async def post_yesterday_results(platinium_channel):
    logger.info("starting post_yesterday_results")
    global vipttips_posted
    # fixme: run in a different thread or coroutine (I don't think this doable cause it uses requests)
    matches_table = get_viptips_results()

    await bot.unpin_message(platinium_channel)

    msg_results_posted = await bot.send_message(platinium_channel, matches_table, reply_to=last_posted_id)

    await bot.pin_message(platinium_channel, msg_results_posted, notify=True)

    vipttips_posted = False

    logger.info("finished with post_yesterday_results")


def time_check(right_now):
    # fix vipttips_posted is not holding it's value
    if right_now.time() >= datetime.time(
        hour=9, minute=0, tzinfo=AA_TIMEZONE) and right_now.time() <= datetime.time(
            hour=9, minute=2, tzinfo=AA_TIMEZONE) and not vipttips_posted:
        return True
    elif right_now.time() >= datetime.time(
        hour=12, minute=0, tzinfo=AA_TIMEZONE) and right_now.time() <= datetime.time(
            hour=12, minute=2, tzinfo=AA_TIMEZONE) and vipttips_posted:
        return True
    else:
        return False


@bot.on(events.NewMessage)
async def send_msg_when_start(event):
    if event.sender_id != 355355326:
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
        logger.info(f"{right_now} -- looping")
        # bot.run_until_disconnected()
