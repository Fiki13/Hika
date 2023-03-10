# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# đ https://github.com/MXRRI/Netfoll

import asyncio
import io
import json
import logging
import random
import time

from telethon.tl import functions
from telethon.tl.tlobject import TLRequest
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall
from ..web.debugger import WebDebugger

logger = logging.getLogger(__name__)

GROUPS = [
    "auth",
    "account",
    "users",
    "contacts",
    "messages",
    "updates",
    "photos",
    "upload",
    "help",
    "channels",
    "bots",
    "payments",
    "stickers",
    "phone",
    "langpack",
    "folders",
    "stats",
]


CONSTRUCTORS = {
    (lambda x: x[0].lower() + x[1:])(
        method.__class__.__name__.rsplit("Request", 1)[0]
    ): method.CONSTRUCTOR_ID
    for method in utils.array_sum(
        [
            [
                method
                for method in dir(getattr(functions, group))
                if isinstance(method, TLRequest)
            ]
            for group in GROUPS
        ]
    )
}


@loader.tds
class APIRatelimiterMod(loader.Module):
    """Helps userbot avoid spamming Telegram API"""

    strings = {
        "name": "APILimiter",
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>WARNING!</b>\n\nYour account exceeded the limit of requests, specified"
            " in config. In order to prevent Telegram API Flood, userbot has been"
            " <b>fully frozen</b> for {} seconds. Further info is provided in attached"
            " file. \n\nIt is recommended to get help in <code>{prefix}support</code>"
            " group!\n\nIf you think, that it is an intended behavior, then wait until"
            " userbot gets unlocked and next time, when you will be going to perform"
            " such an operation, use <code>{prefix}suspend_api_protect</code> &lt;time"
            " in seconds&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Invalid arguments</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>API Flood Protection"
            " is disabled for {} seconds</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection enabled</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection"
            " disabled</b>"
        ),
        "u_sure": "â ī¸ <b>Are you sure?</b>",
        "_cfg_time_sample": "Time sample through which the bot will count requests",
        "_cfg_threshold": "Threshold of requests to trigger protection",
        "_cfg_local_floodwait": (
            "Freeze userbot for this amount of time, if request limit exceeds"
        ),
        "_cfg_forbidden_methods": (
            "Forbid specified methods from being executed throughout external modules"
        ),
        "btn_no": "đĢ No",
        "btn_yes": "â Yes",
        "web_pin": (
            "đ <b>Click the button below to show Werkzeug debug PIN. Do not give it to"
            " anyone.</b>"
        ),
        "web_pin_btn": "đ Show Werkzeug PIN",
        "proxied_url": "đ Proxied URL",
        "local_url": "đ  Local URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web debugger is"
            " disabled, url is not available</b>"
        ),
    }

    strings_ru = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>ĐĐĐĐĐĐĐĐ!</b>\n\nĐĐēĐēĐ°ŅĐŊŅ Đ˛ŅŅĐĩĐģ ĐˇĐ° ĐģĐ¸ĐŧĐ¸ŅŅ ĐˇĐ°ĐŋŅĐžŅĐžĐ˛, ŅĐēĐ°ĐˇĐ°ĐŊĐŊŅĐĩ Đ˛"
            " ĐēĐžĐŊŅĐ¸ĐŗĐĩ. ĐĄ ŅĐĩĐģŅŅ ĐŋŅĐĩĐ´ĐžŅĐ˛ŅĐ°ŅĐĩĐŊĐ¸Ņ ŅĐģŅĐ´Đ° Telegram API, ŅĐˇĐĩŅĐąĐžŅ ĐąŅĐģ"
            " <b>ĐŋĐžĐģĐŊĐžŅŅŅŅ ĐˇĐ°ĐŧĐžŅĐžĐļĐĩĐŊ</b> ĐŊĐ° {} ŅĐĩĐēŅĐŊĐ´. ĐĐžĐŋĐžĐģĐŊĐ¸ŅĐĩĐģŅĐŊĐ°Ņ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ"
            " ĐŋŅĐ¸ĐēŅĐĩĐŋĐģĐĩĐŊĐ° Đ˛ ŅĐ°ĐšĐģĐĩ ĐŊĐ¸ĐļĐĩ. \n\nĐ ĐĩĐēĐžĐŧĐĩĐŊĐ´ŅĐĩŅŅŅ ĐžĐąŅĐ°ŅĐ¸ŅŅŅŅ ĐˇĐ° ĐŋĐžĐŧĐžŅŅŅ Đ˛"
            " <code>{prefix}support</code> ĐŗŅŅĐŋĐŋŅ!\n\nĐŅĐģĐ¸ ŅŅ ŅŅĐ¸ŅĐ°ĐĩŅŅ, ŅŅĐž ŅŅĐž"
            " ĐˇĐ°ĐŋĐģĐ°ĐŊĐ¸ŅĐžĐ˛Đ°ĐŊĐŊĐžĐĩ ĐŋĐžĐ˛ĐĩĐ´ĐĩĐŊĐ¸Đĩ ŅĐˇĐĩŅĐąĐžŅĐ°, ĐŋŅĐžŅŅĐž ĐŋĐžĐ´ĐžĐļĐ´Đ¸, ĐŋĐžĐēĐ° ĐˇĐ°ĐēĐžĐŊŅĐ¸ŅŅŅ"
            " ŅĐ°ĐšĐŧĐĩŅ Đ¸ Đ˛ ŅĐģĐĩĐ´ŅŅŅĐ¸Đš ŅĐ°Đˇ, ĐēĐžĐŗĐ´Đ° ĐˇĐ°ĐŋĐģĐ°ĐŊĐ¸ŅŅĐĩŅŅ Đ˛ŅĐŋĐžĐģĐŊŅŅŅ ŅĐ°ĐēŅŅ"
            " ŅĐĩŅŅŅŅĐžĐˇĐ°ŅŅĐ°ŅĐŊŅŅ ĐžĐŋĐĩŅĐ°ŅĐ¸Ņ, Đ¸ŅĐŋĐžĐģŅĐˇŅĐš"
            " <code>{prefix}suspend_api_protect</code> &lt;Đ˛ŅĐĩĐŧŅ Đ˛ ŅĐĩĐēŅĐŊĐ´Đ°Ņ&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐ˛ĐĩŅĐŊŅĐĩ Đ°ŅĐŗŅĐŧĐĩĐŊŅŅ</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅĐ° API ĐžŅĐēĐģŅŅĐĩĐŊĐ°"
            " ĐŊĐ° {} ŅĐĩĐēŅĐŊĐ´</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅĐ° Đ˛ĐēĐģŅŅĐĩĐŊĐ°</b>",
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅĐ° ĐžŅĐēĐģŅŅĐĩĐŊĐ°</b>"
        ),
        "u_sure": "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>ĐĸŅ ŅĐ˛ĐĩŅĐĩĐŊ?</b>",
        "_cfg_time_sample": (
            "ĐŅĐĩĐŧĐĩĐŊĐŊĐžĐš ĐŋŅĐžĐŧĐĩĐļŅŅĐžĐē, ĐŋĐž ĐēĐžŅĐžŅĐžĐŧŅ ĐąŅĐ´ĐĩŅ ŅŅĐ¸ŅĐ°ŅŅŅŅ ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Đž ĐˇĐ°ĐŋŅĐžŅĐžĐ˛"
        ),
        "_cfg_threshold": "ĐĐžŅĐžĐŗ ĐˇĐ°ĐŋŅĐžŅĐžĐ˛, ĐŋŅĐ¸ ĐēĐžŅĐžŅĐžĐŧ ĐąŅĐ´ĐĩŅ ŅŅĐ°ĐąĐ°ŅŅĐ˛Đ°ŅŅ ĐˇĐ°ŅĐ¸ŅĐ°",
        "_cfg_local_floodwait": (
            "ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ŅĐˇĐĩŅĐąĐžŅĐ° ĐŊĐ° ŅŅĐž ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Đž ŅĐĩĐēŅĐŊĐ´, ĐĩŅĐģĐ¸ ĐģĐ¸ĐŧĐ¸Ņ ĐˇĐ°ĐŋŅĐžŅĐžĐ˛ ĐŋŅĐĩĐ˛ŅŅĐĩĐŊ"
        ),
        "_cfg_forbidden_methods": (
            "ĐĐ°ĐŋŅĐĩŅĐ¸ŅŅ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Đĩ ŅĐēĐ°ĐˇĐ°ĐŊĐŊŅŅ ĐŧĐĩŅĐžĐ´ĐžĐ˛ Đ˛Đž Đ˛ŅĐĩŅ Đ˛ĐŊĐĩŅĐŊĐ¸Ņ ĐŧĐžĐ´ŅĐģŅŅ"
        ),
        "btn_no": "đĢ ĐĐĩŅ",
        "btn_yes": "â ĐĐ°",
        "web_pin": (
            "đ <b>ĐĐ°ĐļĐŧĐ¸ ĐŊĐ° ĐēĐŊĐžĐŋĐēŅ ĐŊĐ¸ĐļĐĩ, ŅŅĐžĐąŅ ĐŋĐžĐēĐ°ĐˇĐ°ŅŅ Werkzeug debug PIN. ĐĐĩ Đ´Đ°Đ˛Đ°Đš ĐĩĐŗĐž"
            " ĐŊĐ¸ĐēĐžĐŧŅ.</b>"
        ),
        "web_pin_btn": "đ ĐĐžĐēĐ°ĐˇĐ°ŅŅ Werkzeug PIN",
        "proxied_url": "đ ĐŅĐžĐēŅĐ¸ŅĐžĐ˛Đ°ĐŊĐŊĐ°Ņ ŅŅŅĐģĐēĐ°",
        "local_url": "đ  ĐĐžĐēĐ°ĐģŅĐŊĐ°Ņ ŅŅŅĐģĐēĐ°",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐą-ĐžŅĐģĐ°Đ´ŅĐ¸Đē ĐžŅĐēĐģŅŅĐĩĐŊ,"
            " ŅŅŅĐģĐēĐ° ĐŊĐĩĐ´ĐžŅŅŅĐŋĐŊĐ°</b>"
        ),
    }

    strings_uk = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            "<b> ŅĐ˛Đ°ĐŗĐ°!</b>\n\N ĐĐēĐēĐ°ŅĐŊŅ Đ˛Đ¸ĐšŅĐžĐ˛ ĐˇĐ° ĐģŅĐŧŅŅĐ¸ ĐˇĐ°ĐŋĐ¸ŅŅĐ˛, ĐˇĐ°ĐˇĐŊĐ°ŅĐĩĐŊŅ Đ˛"
            "ĐēĐžĐŊŅŅĐŗĐĩ. Đ ĐŧĐĩŅĐžŅ ĐˇĐ°ĐŋĐžĐąŅĐŗĐ°ĐŊĐŊŅ ŅĐģŅĐ´Ņ Telegram API, ŅĐˇĐĩŅĐąĐžŅ ĐąŅĐ˛"
            "<b> ĐŋĐžĐ˛ĐŊŅŅŅŅ ĐˇĐ°ĐŧĐžŅĐžĐļĐĩĐŊĐ¸Đš</b> ĐĐ° {} ŅĐĩĐēŅĐŊĐ´. ĐĐžĐ´Đ°ŅĐēĐžĐ˛Đ° ŅĐŊŅĐžŅĐŧĐ°ŅŅŅ"
            "ĐŋŅĐ¸ĐēŅŅĐŋĐģĐĩĐŊĐ° Ņ ŅĐ°ĐšĐģŅ ĐŊĐ¸ĐļŅĐĩ. \n\n ĐŋŅĐĩĐ´ĐēĐžĐŧĐĩĐŊĐ´ŅĐĩŅŅŅ ĐˇĐ˛ĐĩŅĐŊŅŅĐ¸ŅŅ ĐˇĐ° Đ´ĐžĐŋĐžĐŧĐžĐŗĐžŅ Đ˛"
            "<code>{prefix}support</code> ĐŗŅŅĐŋŅ!\n\n ĐŋŅĐēŅĐž ŅĐ¸ Đ˛Đ˛Đ°ĐļĐ°ŅŅ, ŅĐž ŅĐĩ"
            "ĐˇĐ°ĐŋĐģĐ°ĐŊĐžĐ˛Đ°ĐŊĐ° ĐŋĐžĐ˛ĐĩĐ´ŅĐŊĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°, ĐŋŅĐžŅŅĐž ĐŋĐžŅĐĩĐēĐ°Đš, ĐŋĐžĐēĐ¸ ĐˇĐ°ĐēŅĐŊŅĐ¸ŅŅŅŅ"
            "ŅĐ°ĐšĐŧĐĩŅ Ņ ĐŊĐ°ŅŅŅĐŋĐŊĐžĐŗĐž ŅĐ°ĐˇŅ, ĐēĐžĐģĐ¸ ĐˇĐ°ĐŋĐģĐ°ĐŊŅŅŅ Đ˛Đ¸ĐēĐžĐŊŅĐ˛Đ°ŅĐ¸ ŅĐ°ĐēŅ"
            "ŅĐĩŅŅŅŅĐžĐ˛Đ¸ŅŅĐ°ŅĐŊŅ ĐžĐŋĐĩŅĐ°ŅŅŅ, Đ˛Đ¸ĐēĐžŅĐ¸ŅŅĐžĐ˛ŅĐš"
            "<code> {prefix}suspend_api_protect</code> &LT; ŅĐ°Ņ Ņ ŅĐĩĐēŅĐŊĐ´Đ°Ņ &gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐ˛ŅŅĐŊŅ Đ°ŅĐŗŅĐŧĐĩĐŊŅĐ¸</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅŅ API Đ˛Đ¸ĐŧĐēĐŊĐĩĐŊĐž"
            " ĐŊĐ° {} ŅĐĩĐēŅĐŊĐ´</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅŅ Đ˛ĐēĐģŅŅĐĩĐŊĐ°</b>",
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅŅ Đ˛ŅĐ´ĐēĐģŅŅĐĩĐŊĐ¸Đš</b>"
        ),
        "u_sure": "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>ĐĸĐ¸ Đ˛ĐŋĐĩĐ˛ĐŊĐĩĐŊĐ¸Đš?</b>",
        "_cfg_time_sample": (
            "Đ§Đ°ŅĐžĐ˛Đ¸Đš ĐŋŅĐžĐŧŅĐļĐžĐē, ĐˇĐ° ŅĐēĐ¸Đŧ ĐąŅĐ´Đĩ Đ˛Đ˛Đ°ĐļĐ°ŅĐ¸ŅŅ ĐēŅĐģŅĐēŅŅŅŅ ĐˇĐ°ĐŋĐ¸ŅŅĐ˛"
        ),
        "_cfg_threshold": "ĐĐžŅŅĐŗ ĐˇĐ°ĐŋĐ¸ŅŅĐ˛, ĐŋŅĐ¸ ŅĐēĐžĐŧŅ ĐąŅĐ´Đĩ ŅĐŋŅĐ°ŅŅĐžĐ˛ŅĐ˛Đ°ŅĐ¸ ĐˇĐ°ŅĐ¸ŅŅ",
        "_cfg_local_floodwait": (
            "ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅĐ¸ ŅĐˇĐĩŅĐąĐžŅĐ° ĐŊĐ° ŅŅ ĐēŅĐģŅĐēŅŅŅŅ ŅĐĩĐēŅĐŊĐ´, ŅĐēŅĐž ĐģŅĐŧŅŅ ĐˇĐ°ĐŋĐ¸ŅŅĐ˛ ĐŋĐĩŅĐĩĐ˛Đ¸ŅĐĩĐŊĐž"
        ),
        "_cfg_forbidden_methods": (
            "ĐĐ°ĐąĐžŅĐžĐŊĐ¸ŅĐ¸ Đ˛Đ¸ĐēĐžĐŊĐ°ĐŊĐŊŅ ĐˇĐ°ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŧĐĩŅĐžĐ´ŅĐ˛ Ņ Đ˛ŅŅŅ ĐˇĐžĐ˛ĐŊŅŅĐŊŅŅ ĐŧĐžĐ´ŅĐģŅŅ"
        ),
        "btn_no": "đĢ ĐŅ",
        "btn_yes": "â ĐĸĐ°Đē",
        "web_pin": (
            "đ <b>ĐĐ°ŅĐ¸ŅĐŊĐ¸ ĐŊĐ° ĐēĐŊĐžĐŋĐēŅ ĐŊĐ¸ĐļŅĐĩ, ŅĐžĐą ĐŋĐžĐēĐ°ĐˇĐ°ŅĐ¸ Werkzeug Debug PIN. ĐĐĩ Đ´Đ°Đ˛Đ°Đš ĐšĐžĐŗĐž"
            " ĐŊĐ¸ĐēĐžĐŧŅ.</b>"
        ),
        "web_pin_btn": "đ ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐŋĐžĐēĐ°ĐˇĐ°ŅĐ¸ Werkzeug PIN",
        "proxied_url": "đ GŅĐžĐē ĐŋŅĐžĐēŅŅ-ĐŋĐžŅĐ¸ĐģĐ°ĐŊĐŊŅ",
        "local_url": " đ  ĐĐžĐēĐ°ĐģŅĐŊĐĩ ĐŋĐžŅĐ¸ĐģĐ°ĐŊĐŊŅ",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐą-ĐŊĐ°ĐģĐ°ĐŗĐžĐ´ĐļŅĐ˛Đ°Ņ Đ˛Đ¸ĐŧĐēĐŊĐĩĐŊĐž,"
            " ĐŋĐžŅĐ¸ĐģĐ°ĐŊĐŊŅ ĐŊĐĩĐ´ĐžŅŅŅĐŋĐŊĐĩ</b>"
        ),
    }

    _ratelimiter = []
    _suspend_until = 0
    _lock = False

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "time_sample",
                15,
                lambda: self.strings("_cfg_time_sample"),
                validator=loader.validators.Integer(minimum=1),
            ),
            loader.ConfigValue(
                "threshold",
                100,
                lambda: self.strings("_cfg_threshold"),
                validator=loader.validators.Integer(minimum=10),
            ),
            loader.ConfigValue(
                "local_floodwait",
                30,
                lambda: self.strings("_cfg_local_floodwait"),
                validator=loader.validators.Integer(minimum=10, maximum=3600),
            ),
            loader.ConfigValue(
                "forbidden_methods",
                ["joinChannel", "importChatInvite"],
                lambda: self.strings("_cfg_forbidden_methods"),
                validator=loader.validators.MultiChoice(
                    [
                        "sendReaction",
                        "joinChannel",
                        "importChatInvite",
                    ]
                ),
                on_change=lambda: self._client.forbid_constructors(
                    map(
                        lambda x: CONSTRUCTORS[x], self.config["forbidden_constructors"]
                    )
                ),
            ),
        )

    async def client_ready(self):
        asyncio.ensure_future(self._install_protection())

    async def _install_protection(self):
        await asyncio.sleep(30)  # Restart lock
        if hasattr(self._client._call, "_old_call_rewritten"):
            raise loader.SelfUnload("Already installed")

        old_call = self._client._call

        async def new_call(
            sender: "MTProtoSender",  # type: ignore
            request: "TLRequest",  # type: ignore
            ordered: bool = False,
            flood_sleep_threshold: int = None,
        ):
            await asyncio.sleep(random.randint(1, 5) / 100)
            if time.perf_counter() > self._suspend_until and not self.get(
                "disable_protection",
                True,
            ):
                request_name = type(request).__name__
                self._ratelimiter += [[request_name, time.perf_counter()]]

                self._ratelimiter = list(
                    filter(
                        lambda x: time.perf_counter() - x[1]
                        < int(self.config["time_sample"]),
                        self._ratelimiter,
                    )
                )

                if (
                    len(self._ratelimiter) > int(self.config["threshold"])
                    and not self._lock
                ):
                    self._lock = True
                    report = io.BytesIO(
                        json.dumps(
                            self._ratelimiter,
                            indent=4,
                        ).encode("utf-8")
                    )
                    report.name = "local_fw_report.json"

                    await self.inline.bot.send_document(
                        self.tg_id,
                        report,
                        caption=self.strings("warning").format(
                            self.config["local_floodwait"],
                            prefix=self.get_prefix(),
                        ),
                    )

                    # It is intented to use time.sleep instead of asyncio.sleep
                    time.sleep(int(self.config["local_floodwait"]))
                    self._lock = False

            return await old_call(sender, request, ordered, flood_sleep_threshold)

        self._client._call = new_call
        self._client._old_call_rewritten = old_call
        self._client._call._hikka_overwritten = True
        logger.debug("Successfully installed ratelimiter")

    async def on_unload(self):
        if hasattr(self._client, "_old_call_rewritten"):
            self._client._call = self._client._old_call_rewritten
            delattr(self._client, "_old_call_rewritten")
            logger.debug("Successfully uninstalled ratelimiter")

    @loader.command(
        ru_doc="<Đ˛ŅĐĩĐŧŅ Đ˛ ŅĐĩĐēŅĐŊĐ´Đ°Ņ> - ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ĐˇĐ°ŅĐ¸ŅŅ API ĐŊĐ° N ŅĐĩĐēŅĐŊĐ´",
        it_doc="<tempo in secondi> - Congela la protezione API per N secondi",
        de_doc="<Sekunden> - API-Schutz fÃŧr N Sekunden einfrieren",
        tr_doc="<saniye> - API korumasÄąnÄą N saniye dondur",
        uz_doc="<soniya> - API himoyasini N soniya o'zgartirish",
        es_doc="<segundos> - Congela la protecciÃŗn de la API durante N segundos",
        kk_doc="<ŅĐĩĐēŅĐŊĐ´> - API ŌĐžŅŌĐ°ŅŅĐŊ N ŅĐĩĐēŅĐŊĐ´ŅŅĐē ŅĐ°ŌŅŅŅĐ° ŌŌąĐģŅĐŋŅĐ°Ņ",
    )
    async def suspend_api_protect(self, message: Message):
        """<time in seconds> - Suspend API Ratelimiter for n seconds"""
        args = utils.get_args_raw(message)

        if not args or not args.isdigit():
            await utils.answer(message, self.strings("args_invalid"))
            return

        self._suspend_until = time.perf_counter() + int(args)
        await utils.answer(message, self.strings("suspended_for").format(args))

    @loader.command(
        ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ/Đ˛ŅĐēĐģŅŅĐ¸ŅŅ ĐˇĐ°ŅĐ¸ŅŅ API",
        it_doc="Attiva/disattiva la protezione API",
        de_doc="API-Schutz einschalten / ausschalten",
        tr_doc="API korumasÄąnÄą aÃ§ / kapat",
        uz_doc="API himoyasini yoqish / o'chirish",
        es_doc="Activar / desactivar la protecciÃŗn de API",
        kk_doc="API ŌĐžŅŌĐ°ŅŅĐŊ ŌĐžŅŅ / ĐļĐžŅ",
    )
    async def api_fw_protection(self, message: Message):
        """Toggle API Ratelimiter"""
        await self.inline.form(
            message=message,
            text=self.strings("u_sure"),
            reply_markup=[
                {"text": self.strings("btn_no"), "action": "close"},
                {"text": self.strings("btn_yes"), "callback": self._finish},
            ],
        )

    @property
    def _debugger(self) -> WebDebugger:
        return logging.getLogger().handlers[0].web_debugger

    async def _show_pin(self, call: InlineCall):
        await call.answer(f"Werkzeug PIN: {self._debugger.pin}", show_alert=True)

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ PIN Werkzeug",
        it_doc="Mostra il PIN Werkzeug",
        de_doc="PIN-Werkzeug anzeigen",
        tr_doc="PIN aracÄąnÄą gÃļster",
        uz_doc="PIN vositasi ko'rsatish",
        es_doc="Mostrar herramienta PIN",
        kk_doc="PIN ŌŌąŅĐ°ĐģŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def debugger(self, message: Message):
        """Show the Werkzeug PIN"""
        await self.inline.form(
            message=message,
            text=self.strings("web_pin"),
            reply_markup=[
                [
                    {
                        "text": self.strings("web_pin_btn"),
                        "callback": self._show_pin,
                    }
                ],
                [
                    {"text": self.strings("proxied_url"), "url": self._debugger.url},
                    {
                        "text": self.strings("local_url"),
                        "url": f"http://127.0.0.1:{self._debugger.port}",
                    },
                ],
            ],
        )

    async def _finish(self, call: InlineCall):
        state = self.get("disable_protection", True)
        self.set("disable_protection", not state)
        await call.edit(self.strings("on" if state else "off"))
