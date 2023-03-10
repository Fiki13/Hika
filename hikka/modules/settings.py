# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# đ https://github.com/MXRRI/Netfoll

import os

import pyrogram
import telethon
from telethon.extensions.html import CUSTOM_EMOJIS
from telethon.tl.types import Message

from .. import loader, main, utils, version
from ..compat.dragon import DRAGON_EMOJI
from ..inline.types import InlineCall


@loader.tds
class CoreMod(loader.Module):
    """Control core userbot settings"""

    strings = {
        "name": "Settings",
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Too many args</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {} blacklisted"
            " from userbot</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {}"
            " unblacklisted from userbot</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>User {} blacklisted"
            " from userbot</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>User {}"
            " unblacklisted from userbot</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>What should the prefix"
            " be set to?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Prefix must be one"
            " symbol in length</b>"
        ),
        "prefix_set": (
            "{} <b>Command prefix"
            " updated. Type</b> <code>{newprefix}setprefix {oldprefix}</code> <b>to"
            " change it back</b>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias created."
            " Access it with</b> <code>{}</code>"
        ),
        "aliases": "<b>đ Aliases:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Command</b>"
            " <code>{}</code> <b>does not exist</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>You must provide a"
            " command and the alias for it</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>You must provide the"
            " alias name</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>removed</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>does not exist</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Database cleared</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n"
            "<emoji document_id=5188666899860298925>đ</emoji> <b>Hikka:</b> <i>V1.6.1</i>\n<emoji"
            " document_id=6327560044845991305>đž</emoji>"
            " <b>Developers: netfoll.t.me/3</b>"
        ),
        "confirm_cleardb": "â ī¸ <b>Are you sure, that you want to clear database?</b>",
        "cleardb_confirm": "đ Clear database",
        "cancel": "đĢ Cancel",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Who to blacklist?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Who to"
            " unblacklist?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>You are using an"
            " unstable branch</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>Your Dragon and Netfoll"
            " prefixes must be different!</b>"
        ),
    }

    strings_ru = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĄĐģĐ¸ŅĐēĐžĐŧ ĐŧĐŊĐžĐŗĐž"
            " Đ°ŅĐŗŅĐŧĐĩĐŊŅĐžĐ˛</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} Đ´ĐžĐąĐ°Đ˛ĐģĐĩĐŊ Đ˛"
            " ŅĐĩŅĐŊŅĐš ŅĐŋĐ¸ŅĐžĐē ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} ŅĐ´Đ°ĐģĐĩĐŊ Đ¸Đˇ"
            " ŅĐĩŅĐŊĐžĐŗĐž ŅĐŋĐ¸ŅĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ {}"
            " Đ´ĐžĐąĐ°Đ˛ĐģĐĩĐŊ Đ˛ ŅĐĩŅĐŊŅĐš ŅĐŋĐ¸ŅĐžĐē ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ {}"
            " ŅĐ´Đ°ĐģĐĩĐŊ Đ¸Đˇ ŅĐĩŅĐŊĐžĐŗĐž ŅĐŋĐ¸ŅĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Đ ĐēĐ°ĐēĐžĐš ĐŋŅĐĩŅĐ¸ĐēŅ"
            " ŅŅĐ°Đ˛Đ¸ŅŅ ŅĐž?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŅĐĩŅĐ¸ĐēŅ Đ´ĐžĐģĐļĐĩĐŊ"
            " ŅĐžŅŅĐžŅŅŅ ŅĐžĐģŅĐēĐž Đ¸Đˇ ĐžĐ´ĐŊĐžĐŗĐž ŅĐ¸ĐŧĐ˛ĐžĐģĐ°</b>"
        ),
        "prefix_set": (
            "{} <b>ĐŅŅŅĐ°Đ˛ĐģĐĩĐŊ ĐŊĐžĐ˛ŅĐš ĐŋŅĐĩŅĐ¸ĐēŅ,"
            " Đ´ĐģŅ ŅĐžĐŗĐž ŅŅĐžĐąŅ Đ˛ĐĩŅĐŊŅŅŅ ŅŅĐ°ŅŅĐš ĐŋŅĐĩŅĐ¸ĐēŅ Đ¸ŅĐŋĐžĐģŅĐˇŅĐš</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģĐ¸Đ°Ņ ŅĐžĐˇĐ´Đ°ĐŊ."
            " ĐŅĐŋĐžĐģŅĐˇŅĐš ĐĩĐŗĐž ŅĐĩŅĐĩĐˇ</b> <code>{}</code>"
        ),
        "aliases": "<b>đ ĐĐģĐ¸Đ°ŅŅ:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ°</b>"
            " <code>{}</code> <b>ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĸŅĐĩĐąŅĐĩŅŅŅ Đ˛Đ˛ĐĩŅŅĐ¸"
            " ĐēĐžĐŧĐ°ĐŊĐ´Ņ Đ¸ Đ°ĐģĐ¸Đ°Ņ Đ´ĐģŅ ĐŊĐĩĐĩ</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĸŅĐĩĐąŅĐĩŅŅŅ Đ¸ĐŧŅ"
            " Đ°ĐģĐ¸Đ°ŅĐ°</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģĐ¸Đ°Ņ</b>"
            " <code>{}</code> <b>ŅĐ´Đ°ĐģĐĩĐŊ</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐģĐ¸Đ°Ņ</b>"
            " <code>{}</code> <b>ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐ°ĐˇĐ° ĐžŅĐ¸ŅĐĩĐŊĐ°</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n"
            "<emoji document_id=5188666899860298925>đ</emoji> <b>Hikka:</b> <i>V1.6.1</i>\n<emoji"
            " document_id=6327560044845991305>đž</emoji>"
            " <b>Đ Đ°ĐˇŅĐ°ĐąĐžŅŅĐ¸ĐēĐ¸: netfoll.t.me/3</b>"
        ),
        "_cls_doc": "ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐąĐ°ĐˇĐžĐ˛ŅĐŧĐ¸ ĐŊĐ°ŅŅŅĐžĐšĐēĐ°ĐŧĐ¸ ŅĐˇĐĩŅĐąĐžŅĐ°",
        "confirm_cleardb": "â ī¸ <b>ĐŅ ŅĐ˛ĐĩŅĐĩĐŊŅ, ŅŅĐž ŅĐžŅĐ¸ŅĐĩ ŅĐąŅĐžŅĐ¸ŅŅ ĐąĐ°ĐˇŅ Đ´Đ°ĐŊĐŊŅŅ?</b>",
        "cleardb_confirm": "đ ĐŅĐ¸ŅŅĐ¸ŅŅ ĐąĐ°ĐˇŅ",
        "cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐĐžĐŗĐž ĐˇĐ°ĐąĐģĐžĐēĐ¸ŅĐžĐ˛Đ°ŅŅ"
            " ŅĐž?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐĐžĐŗĐž ŅĐ°ĐˇĐąĐģĐžĐēĐ¸ŅĐžĐ˛Đ°ŅŅ"
            " ŅĐž?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=6334517075821725662>đ</emoji> <b>ĐŅĐŋĐžĐģŅĐˇŅĐĩŅŅŅ"
            " ĐŊĐĩŅŅĐ°ĐąĐ¸ĐģŅĐŊĐ°Ņ Đ˛ĐĩŅĐēĐ°</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>ĐŅĐĩŅĐ¸ĐēŅŅ Dragon Đ¸"
            " Netfoll Đ´ĐžĐģĐļĐŊŅ ĐžŅĐģĐ¸ŅĐ°ŅŅŅŅ!</b>"
        ),
    }

    strings_uk = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐ°Đ´ŅĐž ĐŧĐŊĐžĐŗĐž"
            " Đ°ŅĐŗŅĐŧĐĩĐŊŅĐžĐ˛</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} Đ´ĐžĐ´Đ°ĐŊĐž Đ˛"
            " ŅĐžŅĐŊĐ¸Đš ŅĐŋĐ¸ŅĐžĐē ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} Đ˛Đ¸Đ´Đ°ĐģĐĩĐŊĐž Đˇ"
            " ŅĐžŅĐŊĐžĐŗĐž ŅĐŋĐ¸ŅĐēŅ ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐžŅĐ¸ŅŅŅĐ˛Đ°Ņ {}"
            " Đ´ĐžĐąĐ°Đ˛ĐģĐĩĐŊ Đ˛ ŅĐžŅĐŊĐ¸Đš ŅĐŋĐ¸ŅĐžĐē ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐžŅĐ¸ŅŅŅĐ˛Đ°Ņ {}"
            " ŅĐ´Đ°ĐģĐĩĐŊ Đ¸Đˇ ŅĐžŅĐŊĐžĐŗĐž ŅĐŋĐ¸ŅĐēŅ ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Đ ŅĐēĐ¸Đš ĐŋŅĐĩŅŅĐēŅ"
            " ŅŅĐ°Đ˛Đ¸ŅĐ¸ ŅĐž?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŅĐĩŅŅĐēŅ ĐŋĐžĐ˛Đ¸ĐŊĐĩĐŊ"
            " ŅĐēĐģĐ°Đ´Đ°ŅĐ¸ŅŅ ŅŅĐģŅĐēĐ¸ Đˇ ĐžĐ´ĐŊĐžĐŗĐž ŅĐ¸ĐŧĐ˛ĐžĐģŅ</b>"
        ),
        "prefix_set": (
            "{} <b>ĐĐ¸ŅŅĐ°Đ˛ĐģĐĩĐŊĐž ĐŊĐžĐ˛Đ¸Đš ĐŋŅĐĩŅŅĐēŅ,"
            " Đ´ĐģŅ ŅĐžĐŗĐž ŅĐžĐą ĐŋĐžĐ˛ĐĩŅĐŊŅŅĐ¸ ŅŅĐ°ŅĐ¸Đš ĐŋŅĐĩŅŅĐēŅ Đ˛Đ¸ĐēĐžŅĐ¸ŅŅĐžĐ˛ŅĐš</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģŅĐ°Ņ ŅŅĐ˛ĐžŅĐĩĐŊĐ¸Đš."
            " ĐĐ¸ĐēĐžŅĐ¸ŅŅĐžĐ˛ŅĐš ĐšĐžĐŗĐž ŅĐĩŅĐĩĐˇ</b> <code>{}</code>"
        ),
        "aliases": "<b>đ ĐĐģŅĐ°ŅĐ¸:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ°</b>"
            " <code>{}</code> <b>ĐŊĐĩ ŅŅĐŊŅŅ</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžŅŅŅĐąĐŊĐž Đ˛Đ˛ĐĩŅŅĐ¸"
            " ĐēĐžĐŧĐ°ĐŊĐ´Ņ Ņ Đ°ĐģŅĐ°Ņ Đ´ĐģŅ ĐŊĐĩŅ</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžŅŅŅĐąĐŊĐĩ ŅĐŧ'Ņ"
            " Đ°ĐģĐ¸Đ°ŅĐ°</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģŅĐ°Ņ</b>"
            " <code>{}</code> <b>Đ˛Đ¸Đ´Đ°ĐģŅŅĐ¸</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐģŅĐ°Ņ</b>"
            " <code>{}</code> <b>ĐŊĐĩ ŅŅĐŊŅŅ</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐ°ĐˇĐ° ĐžŅĐ¸ŅĐĩĐŊĐ°</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n"
            "<emoji document_id=5188666899860298925>đ</emoji> <b>Hikka:</b> <i>V1.6.1</i>\n<emoji"
            " document_id=6327560044845991305>đž</emoji>"
            " <b>Đ ĐžĐˇŅĐžĐąĐŊĐ¸ĐēĐ¸: netfoll.t.me/3</b>"
        ),
        "_cls_doc": "ĐŖĐŋŅĐ°Đ˛ĐģŅĐŊĐŊŅ ĐąĐ°ĐˇĐžĐ˛Đ¸ĐŧĐ¸ ĐŊĐ°ŅŅŅĐžĐšĐēĐ°ĐŧĐ¸ ŅĐˇĐĩŅĐąĐžŅĐ°",
        "confirm_cleardb": "â ī¸ <b>ĐĐ¸ Đ˛ĐŋĐĩĐ˛ĐŊĐĩĐŊŅ, ŅĐž ŅĐžŅĐĩŅĐĩ ŅĐēĐ¸ĐŊŅŅĐ¸ ĐąĐ°ĐˇŅ Đ´Đ°ĐŊĐ¸Ņ?</b>",
        "cleardb_confirm": "đ ĐŅĐ¸ŅŅĐ¸ŅĐ¸ ĐąĐ°ĐˇŅ",
        "cancel": "đĢ ĐĄĐēĐ°ŅŅĐ˛Đ°ĐŊĐŊŅ",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐĐžĐŗĐž ĐˇĐ°ĐąĐģĐžĐēŅĐ˛Đ°ŅĐ¸"
            " ŅĐž?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐĐžĐŗĐž ŅĐžĐˇĐąĐģĐžĐēŅĐ˛Đ°ŅĐ¸"
            " ŅĐž?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=6334517075821725662>đ</emoji> <b>ĐĐ¸ĐēĐžŅĐ¸ŅŅĐžĐ˛ŅĐ˛Đ°ŅĐ¸"
            " ĐŊĐĩŅŅĐ°ĐąŅĐģŅĐŊĐ° ĐŗŅĐģĐēĐ°</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>ĐŅĐĩŅŅĐēŅĐ¸ Dragon Ņ"
            " Netfoll ĐŋĐžĐ˛Đ¸ĐŊĐŊŅ Đ˛ŅĐ´ŅŅĐˇĐŊŅŅĐ¸ŅŅ!</b>"
        ),
    }    

    async def blacklistcommon(self, message: Message):
        args = utils.get_args(message)

        if len(args) > 2:
            await utils.answer(message, self.strings("too_many_args"))
            return

        chatid = None
        module = None

        if args:
            try:
                chatid = int(args[0])
            except ValueError:
                module = args[0]

        if len(args) == 2:
            module = args[1]

        if chatid is None:
            chatid = utils.get_chat_id(message)

        module = self.allmodules.get_classname(module)
        return f"{str(chatid)}.{module}" if module else chatid

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ˛ĐĩŅŅĐ¸Ņ Netfoll",
    )
    async def netfollcmd(self, message: Message):
        """Get Netfoll version"""
        await utils.answer_file(
            message,
            "https://github.com/MXRRI/Netfoll/raw/stable/assets/banner.png",
            self.strings("hikka").format(
                (
                    (
                        utils.get_platform_emoji(self._client)
                        + (
                            ""
                            if "LAVHOST" in os.environ
                            else ""
                        )
                    )
                    if self._client.hikka_me.premium and CUSTOM_EMOJIS
                    else "đž <b>Netfoll</b>"
                ),
                *version.netver,
                utils.get_commit_url(),
                f"{telethon.__version__} #{telethon.tl.alltlobjects.LAYER}",
                (
                    "<emoji document_id=5377399247589088543>đĨ</emoji>"
                    if self._client.pyro_proxy
                    else "<emoji document_id=5418308381586759720>đ´</emoji>"
                ),
                f"{pyrogram.__version__} #{pyrogram.raw.all.layer}",
            )
            + (
                ""
                if version.branch == "stable"
                else self.strings("unstable").format(version.branch)
            ),
        )

    @loader.command(
        ru_doc="[ŅĐ°Ņ] [ĐŧĐžĐ´ŅĐģŅ] - ĐŅĐēĐģŅŅĐ¸ŅŅ ĐąĐžŅĐ° ĐŗĐ´Đĩ-ĐģĐ¸ĐąĐž",
    )
    async def blacklist(self, message: Message):
        """[chat_id] [module] - Blacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            self._db.get(main.__name__, "blacklist_chats", []) + [chatid],
        )

        await utils.answer(message, self.strings("blacklisted").format(chatid))

    @loader.command(
        ru_doc="[ŅĐ°Ņ] - ĐĐēĐģŅŅĐ¸ŅŅ ĐąĐžŅĐ° ĐŗĐ´Đĩ-ĐģĐ¸ĐąĐž",
    )
    async def unblacklist(self, message: Message):
        """<chat_id> - Unblacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            list(set(self._db.get(main.__name__, "blacklist_chats", [])) - {chatid}),
        )

        await utils.answer(message, self.strings("unblacklisted").format(chatid))

    async def getuser(self, message: Message):
        try:
            return int(utils.get_args(message)[0])
        except (ValueError, IndexError):
            reply = await message.get_reply_message()

            if reply:
                return reply.sender_id

            return message.to_id.user_id if message.is_private else False

    @loader.command(
        ru_doc="[ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ] - ĐĐ°ĐŋŅĐĩŅĐ¸ŅŅ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ Đ˛ŅĐŋĐžĐģĐŊŅŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
    )
    async def blacklistuser(self, message: Message):
        """[user_id] - Prevent this user from running any commands"""
        user = await self.getuser(message)

        if not user:
            await utils.answer(message, self.strings("who_to_blacklist"))
            return

        self._db.set(
            main.__name__,
            "blacklist_users",
            self._db.get(main.__name__, "blacklist_users", []) + [user],
        )

        await utils.answer(message, self.strings("user_blacklisted").format(user))

    @loader.command(
        ru_doc="[ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ] - Đ Đ°ĐˇŅĐĩŅĐ¸ŅŅ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ Đ˛ŅĐŋĐžĐģĐŊŅŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
    )
    async def unblacklistuser(self, message: Message):
        """[user_id] - Allow this user to run permitted commands"""
        user = await self.getuser(message)

        if not user:
            await utils.answer(message, self.strings("who_to_unblacklist"))
            return

        self._db.set(
            main.__name__,
            "blacklist_users",
            list(set(self._db.get(main.__name__, "blacklist_users", [])) - {user}),
        )

        await utils.answer(
            message,
            self.strings("user_unblacklisted").format(user),
        )

    @loader.owner
    @loader.command(
        ru_doc="[dragon] <ĐŋŅĐĩŅĐ¸ĐēŅ> - ĐŖŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ ĐŋŅĐĩŅĐ¸ĐēŅ ĐēĐžĐŧĐ°ĐŊĐ´",
    )
    async def setprefix(self, message: Message):
        """[dragon] <prefix> - Sets command prefix"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings("what_prefix"))
            return

        if len(args.split()) == 2 and args.split()[0] == "dragon":
            args = args.split()[1]
            is_dragon = True
        else:
            is_dragon = False

        if len(args) != 1:
            await utils.answer(message, self.strings("prefix_incorrect"))
            return

        if (
            not is_dragon
            and args[0] == self._db.get("dragon.prefix", "command_prefix", ",")
            or is_dragon
            and args[0] == self._db.get(main.__name__, "command_prefix", ".")
        ):
            await utils.answer(message, self.strings("prefix_collision"))
            return

        oldprefix = (
            f"dragon {self.get_prefix('dragon')}" if is_dragon else self.get_prefix()
        )
        self._db.set(
            "dragon.prefix" if is_dragon else main.__name__,
            "command_prefix",
            args,
        )
        await utils.answer(
            message,
            self.strings("prefix_set").format(
                (
                    DRAGON_EMOJI
                    if is_dragon
                    else "<emoji document_id=5370869711888194012>đž</emoji>"
                ),
                newprefix=utils.escape_html(
                    self.get_prefix() if is_dragon else args[0]
                ),
                oldprefix=utils.escape_html(oldprefix),
            ),
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐģĐ¸Đ°ŅĐžĐ˛",
    )
    async def aliases(self, message: Message):
        """Print all your aliases"""
        aliases = self.allmodules.aliases
        string = self.strings("aliases")

        string += "\n".join(
            [f"âĢī¸ <code>{i}</code> &lt;- {y}" for i, y in aliases.items()]
        )

        await utils.answer(message, string)

    @loader.owner
    @loader.command(
        ru_doc="ĐŖŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ Đ°ĐģĐ¸Đ°Ņ Đ´ĐģŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
    )
    async def addalias(self, message: Message):
        """Set an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 2:
            await utils.answer(message, self.strings("alias_args"))
            return

        alias, cmd = args
        if self.allmodules.add_alias(alias, cmd):
            self.set(
                "aliases",
                {
                    **self.get("aliases", {}),
                    alias: cmd,
                },
            )
            await utils.answer(
                message,
                self.strings("alias_created").format(utils.escape_html(alias)),
            )
        else:
            await utils.answer(
                message,
                self.strings("no_command").format(utils.escape_html(cmd)),
            )

    @loader.owner
    @loader.command(
        ru_doc="ĐŖĐ´Đ°ĐģĐ¸ŅŅ Đ°ĐģĐ¸Đ°Ņ Đ´ĐģŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
    )
    async def delalias(self, message: Message):
        """Remove an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 1:
            await utils.answer(message, self.strings("delalias_args"))
            return

        alias = args[0]
        removed = self.allmodules.remove_alias(alias)

        if not removed:
            await utils.answer(
                message,
                self.strings("no_alias").format(utils.escape_html(alias)),
            )
            return

        current = self.get("aliases", {})
        del current[alias]
        self.set("aliases", current)
        await utils.answer(
            message,
            self.strings("alias_removed").format(utils.escape_html(alias)),
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐŅĐ¸ŅŅĐ¸ŅŅ ĐąĐ°ĐˇŅ Đ´Đ°ĐŊĐŊŅŅ",
    )
    async def cleardb(self, message: Message):
        """Clear the entire database, effectively performing a factory reset"""
        await self.inline.form(
            self.strings("confirm_cleardb"),
            message,
            reply_markup=[
                {
                    "text": self.strings("cleardb_confirm"),
                    "callback": self._inline__cleardb,
                },
                {
                    "text": self.strings("cancel"),
                    "action": "close",
                },
            ],
        )

    async def _inline__cleardb(self, call: InlineCall):
        self._db.clear()
        self._db.save()
        await utils.answer(call, self.strings("db_cleared"))
