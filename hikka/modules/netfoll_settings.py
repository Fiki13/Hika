# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# đ https://github.com/MXRRI/Netfoll


import logging
import os
import random

import telethon
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, log, main, utils
from .._internal import fw_protect, restart
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

ALL_INVOKES = [
    "clear_entity_cache",
    "clear_fulluser_cache",
    "clear_fullchannel_cache",
    "clear_perms_cache",
    "clear_cache",
    "reload_core",
    "inspect_cache",
    "inspect_modules",
]


@loader.tds
class NetfollSettingsMod(loader.Module):
    """Advanced settings for Hikka Userbot"""

    strings = {
        "name": "NetfollSettings",
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Watchers:</b>\n\n<b>{}</b>"
        ),
        "no_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>No arguments"
            " specified</b>"
        ),
        "invoke404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Internal debug method"
            "</b> <code>{}</code> <b>not found, ergo can't be invoked</b>"
        ),
        "module404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Module</b>"
            " <code>{}</code> <b>not found</b>"
        ),
        "invoke": (
            "<emoji document_id=5215519585150706301>đ</emoji> <b>Invoked internal debug"
            " method</b> <code>{}</code>\n\n<emoji"
            " document_id=5784891605601225888>đĩ</emoji> <b>Result:\n{}</b>"
        ),
        "invoking": (
            "<emoji document_id=5213452215527677338>âŗ</emoji> <b>Invoking internal"
            " debug method</b> <code>{}</code> <b>of</b> <code>{}</code><b>...</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Watcher {} not"
            " found</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Watcher {} is now"
            " <u>disabled</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Watcher {} is now"
            " <u>enabled</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>You need to specify"
            " watcher name</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick for this user"
            " is now {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Please, specify"
            " command to toggle NoNick for</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick for"
            "</b> <code>{}</code> <b>is now {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Command not found</b>"
        ),
        "inline_settings": "âī¸ <b>Here you can configure your Netfoll settings</b>",
        "confirm_update": (
            "đ§­ <b>Please, confirm that you want to update. Your userbot will be"
            " restarted</b>"
        ),
        "confirm_restart": "đ <b>Please, confirm that you want to restart</b>",
        "suggest_fs": "â Suggest FS for modules",
        "do_not_suggest_fs": "đĢ Suggest FS for modules",
        "use_fs": "â Always use FS for modules",
        "do_not_use_fs": "đĢ Always use FS for modules",
        "btn_restart": "đ Restart",
        "btn_update": "đ§­ Update",
        "close_menu": "đ Close menu",
        "custom_emojis": "â Custom emojis",
        "no_custom_emojis": "đĢ Custom emojis",
        "suggest_subscribe": "â Suggest subscribe to channel",
        "do_not_suggest_subscribe": "đĢ Suggest subscribe to channel",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>This command must be"
            " executed in chat</b>"
        ),
        "nonick_warning": (
            "Warning! You enabled NoNick with default prefix! "
            "You may get muted in Netfoll chats. Change prefix or "
            "disable NoNick!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Reply to a message"
            " of user, which needs to be added to NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>This action will fully remove Netfoll from this account and can't be"
            " reverted!</b>\n\n<i>- Netfoll chats will be removed\n- Session will be"
            " terminated and removed\n- Netfoll inline bot will be removed</i>"
        ),
        "deauth_confirm_step2": (
            "â ī¸ <b>Are you really sure you want to delete Netfoll?</b>"
        ),
        "deauth_yes": "I'm sure",
        "deauth_no_1": "I'm not sure",
        "deauth_no_2": "I'm uncertain",
        "deauth_no_3": "I'm struggling to answer",
        "deauth_cancel": "đĢ Cancel",
        "deauth_confirm_btn": "đĸ Delete",
        "uninstall": "đĸ <b>Uninstalling Netfoll...</b>",
        "uninstalled": (
            "đĸ <b>Netfoll uninstalled. Web interface is still active, you can add another"
            " account</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick is enabled"
            " for these commands:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick is enabled"
            " for these users:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick is enabled"
            " for these chats:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Nothing to"
            " show...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>This command gives access to your Netfoll web interface. It's not"
            " recommended to run it in public group chats. Consider using it in <a"
            " href='tg://openmessage?user_id={}'>Saved messages</a>. Type"
            "</b> <code>{}proxypass force_insecure</code> <b>to ignore this warning</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>This command gives access to your Netfoll web interface. It's not"
            " recommended to run it in public group chats. Consider using it in <a"
            " href='tg://openmessage?user_id={}'>Saved messages</a>.</b>"
        ),
        "opening_tunnel": "đ <b>Opening tunnel to Netfoll web interface...</b>",
        "tunnel_opened": "đ <b>Tunnel opened. This link is valid for about 1 hour</b>",
        "web_btn": "đ Web interface",
        "btn_yes": "đ¸ Open anyway",
        "btn_no": "đģ Cancel",
        "lavhost_web": (
            "âī¸ <b>This link leads to your Netfoll web interface on lavHost</b>\n\n<i>đĄ"
            " You'll need to authorize using lavHost credentials, specified on"
            " registration</i>"
        ),
        "disable_debugger": "â Debugger enabled",
        "enable_debugger": "đĢ Debugger disabled",
    }

    strings_ru = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģĐ¸:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģŅ {} ĐŊĐĩ"
            " ĐŊĐ°ĐšĐ´ĐĩĐŊ</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģŅ {} ŅĐĩĐŋĐĩŅŅ"
            " <u>Đ˛ŅĐēĐģŅŅĐĩĐŊ</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģŅ {} ŅĐĩĐŋĐĩŅŅ"
            " <u>Đ˛ĐēĐģŅŅĐĩĐŊ</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŖĐēĐ°ĐļĐ¸ Đ¸ĐŧŅ"
            " ŅĐŧĐžŅŅĐ¸ŅĐĩĐģŅ</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĄĐžŅŅĐžŅĐŊĐ¸Đĩ NoNick Đ´ĐģŅ"
            " ŅŅĐžĐŗĐž ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐŖĐēĐ°ĐļĐ¸ ĐēĐžĐŧĐ°ĐŊĐ´Ņ, Đ´ĐģŅ"
            " ĐēĐžŅĐžŅĐžĐš ĐŊĐ°Đ´Đž Đ˛ĐēĐģŅŅĐ¸ŅŅ\\Đ˛ŅĐēĐģŅŅĐ¸ŅŅ NoNick</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĄĐžŅŅĐžŅĐŊĐ¸Đĩ NoNick Đ´ĐģŅ"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ° ĐŊĐĩ ĐŊĐ°ĐšĐ´ĐĩĐŊĐ°</b>"
        ),
        "inline_settings": "âī¸ <b>ĐĐ´ĐĩŅŅ ĐŧĐžĐļĐŊĐž ŅĐŋŅĐ°Đ˛ĐģŅŅŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ°ĐŧĐ¸ Netfoll</b>",
        "confirm_update": "đ§­ <b>ĐĐžĐ´ŅĐ˛ĐĩŅĐ´Đ¸ŅĐĩ ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đĩ. ĐŽĐˇĐĩŅĐąĐžŅ ĐąŅĐ´ĐĩŅ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐļĐĩĐŊ</b>",
        "confirm_restart": "đ <b>ĐĐžĐ´ŅĐ˛ĐĩŅĐ´Đ¸ŅĐĩ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēŅ</b>",
        "suggest_fs": "â ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ŅĐžŅŅĐ°ĐŊĐĩĐŊĐ¸Đĩ ĐŧĐžĐ´ŅĐģĐĩĐš",
        "do_not_suggest_fs": "đĢ ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ŅĐžŅŅĐ°ĐŊĐĩĐŊĐ¸Đĩ ĐŧĐžĐ´ŅĐģĐĩĐš",
        "use_fs": "â ĐŅĐĩĐŗĐ´Đ° ŅĐžŅŅĐ°ĐŊŅŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        "do_not_use_fs": "đĢ ĐŅĐĩĐŗĐ´Đ° ŅĐžŅŅĐ°ĐŊŅŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        "btn_restart": "đ ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ°",
        "btn_update": "đ§­ ĐĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đĩ",
        "close_menu": "đ ĐĐ°ĐēŅŅŅŅ ĐŧĐĩĐŊŅ",
        "custom_emojis": "â ĐĐ°ŅŅĐžĐŧĐŊŅĐĩ ŅĐŧĐžĐ´ĐˇĐ¸",
        "no_custom_emojis": "đĢ ĐĐ°ŅŅĐžĐŧĐŊŅĐĩ ŅĐŧĐžĐ´ĐˇĐ¸",
        "suggest_subscribe": "â ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ĐŋĐžĐ´ĐŋĐ¸ŅĐēŅ ĐŊĐ° ĐēĐ°ĐŊĐ°Đģ",
        "do_not_suggest_subscribe": "đĢ ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ĐŋĐžĐ´ĐŋĐ¸ŅĐēŅ ĐŊĐ° ĐēĐ°ĐŊĐ°Đģ",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Đ­ŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ ĐŊŅĐļĐŊĐž"
            " Đ˛ŅĐŋĐžĐģĐŊŅŅŅ Đ˛ ŅĐ°ŅĐĩ</b>"
        ),
        "_cls_doc": "ĐĐžĐŋĐžĐģĐŊĐ¸ŅĐĩĐģŅĐŊŅĐĩ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸ Netfoll",
        "nonick_warning": (
            "ĐĐŊĐ¸ĐŧĐ°ĐŊĐ¸Đĩ! ĐĸŅ Đ˛ĐēĐģŅŅĐ¸Đģ NoNick ŅĐž ŅŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅĐŧ ĐŋŅĐĩŅĐ¸ĐēŅĐžĐŧ! "
            "ĐĸĐĩĐąŅ ĐŧĐžĐŗŅŅ ĐˇĐ°ĐŧŅŅŅĐ¸ŅŅ Đ˛ ŅĐ°ŅĐ°Ņ Netfoll. ĐĐˇĐŧĐĩĐŊĐ¸ ĐŋŅĐĩŅĐ¸ĐēŅ Đ¸ĐģĐ¸ "
            "ĐžŅĐēĐģŅŅĐ¸ ĐŗĐģĐžĐąĐ°ĐģŅĐŊŅĐš NoNick!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŅĐ˛ĐĩŅŅ ĐŊĐ° ŅĐžĐžĐąŅĐĩĐŊĐ¸Đĩ"
            " ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ, Đ´ĐģŅ ĐēĐžŅĐžŅĐžĐŗĐž ĐŊŅĐļĐŊĐž Đ˛ĐēĐģŅŅĐ¸ŅŅ NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Đ­ŅĐž Đ´ĐĩĐšŅŅĐ˛Đ¸Đĩ ĐŋĐžĐģĐŊĐžŅŅŅŅ ŅĐ´Đ°ĐģĐ¸Ņ Netfoll Ņ ŅŅĐžĐŗĐž Đ°ĐēĐēĐ°ŅĐŊŅĐ°! ĐĐŗĐž ĐŊĐĩĐģŅĐˇŅ"
            " ĐžŅĐŧĐĩĐŊĐ¸ŅŅ</b>\n\n<i>- ĐŅĐĩ ŅĐ°ŅŅ, ŅĐ˛ŅĐˇĐ°ĐŊĐŊŅĐĩ Ņ Netfoll ĐąŅĐ´ŅŅ ŅĐ´Đ°ĐģĐĩĐŊŅ\n- ĐĄĐĩŅŅĐ¸Ņ"
            " Netfoll ĐąŅĐ´ĐĩŅ ŅĐąŅĐžŅĐĩĐŊĐ°\n- ĐĐŊĐģĐ°ĐšĐŊ ĐąĐžŅ Netfoll ĐąŅĐ´ĐĩŅ ŅĐ´Đ°ĐģĐĩĐŊ</i>"
        ),
        "deauth_confirm_step2": "â ī¸ <b>ĐĸŅ ŅĐžŅĐŊĐž ŅĐ˛ĐĩŅĐĩĐŊ, ŅŅĐž ŅĐžŅĐĩŅŅ ŅĐ´Đ°ĐģĐ¸ŅŅ Netfoll?</b>",
        "deauth_yes": "Đ¯ ŅĐ˛ĐĩŅĐĩĐŊ",
        "deauth_no_1": "Đ¯ ĐŊĐĩ ŅĐ˛ĐĩŅĐĩĐŊ",
        "deauth_no_2": "ĐĐĩ ŅĐžŅĐŊĐž",
        "deauth_no_3": "ĐĐĩŅ",
        "deauth_cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
        "deauth_confirm_btn": "đĸ ĐŖĐ´Đ°ĐģĐ¸ŅŅ",
        "uninstall": "đĸ <b>ĐŖĐ´Đ°ĐģŅŅ Netfoll...</b>",
        "uninstalled": (
            "đĸ <b>Netfoll ŅĐ´Đ°ĐģĐĩĐŊĐ°. ĐĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ Đ˛ŅĐĩ ĐĩŅĐĩ Đ°ĐēŅĐ¸Đ˛ĐĩĐŊ, ĐŧĐžĐļĐŊĐž Đ´ĐžĐąĐ°Đ˛Đ¸ŅŅ Đ´ŅŅĐŗĐ¸Đĩ"
            " Đ°ĐēĐēĐ°ŅĐŊŅŅ!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ"
            " ŅŅĐ¸Ņ ĐēĐžĐŧĐ°ĐŊĐ´:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ"
            " ŅŅĐ¸Ņ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģĐĩĐš:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ"
            " ŅŅĐ¸Ņ ŅĐ°ŅĐžĐ˛:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>ĐĐĩŅĐĩĐŗĐž"
            " ĐŋĐžĐēĐ°ĐˇŅĐ˛Đ°ŅŅ...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Đ­ŅĐ° ĐēĐžĐŧĐ°ĐŊĐ´Đ° Đ´Đ°ĐĩŅ Đ´ĐžŅŅŅĐŋ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Netfoll. ĐĐĩ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Đĩ Đ˛"
            " ĐŋŅĐąĐģĐ¸ŅĐŊŅŅ ŅĐ°ŅĐ°Ņ ŅĐ˛ĐģŅĐĩŅŅŅ ŅĐŗŅĐžĐˇĐžĐš ĐąĐĩĐˇĐžĐŋĐ°ŅĐŊĐžŅŅĐ¸. ĐŅĐĩĐ´ĐŋĐžŅŅĐ¸ŅĐĩĐģŅĐŊĐž Đ˛ŅĐŋĐžĐģĐŊŅŅŅ"
            " ĐĩĐĩ Đ˛ <a href='tg://openmessage?user_id={}'>ĐĐˇĐąŅĐ°ĐŊĐŊŅŅ ŅĐžĐžĐąŅĐĩĐŊĐ¸ŅŅ</a>."
            " ĐŅĐŋĐžĐģĐŊĐ¸</b> <code>{}proxypass force_insecure</code> <b>ŅŅĐžĐąŅ ĐžŅĐēĐģŅŅĐ¸ŅŅ"
            " ŅŅĐž ĐŋŅĐĩĐ´ŅĐŋŅĐĩĐļĐ´ĐĩĐŊĐ¸Đĩ</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Đ­ŅĐ° ĐēĐžĐŧĐ°ĐŊĐ´Đ° Đ´Đ°ĐĩŅ Đ´ĐžŅŅŅĐŋ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Netfoll. ĐĐĩ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Đĩ Đ˛"
            " ĐŋŅĐąĐģĐ¸ŅĐŊŅŅ ŅĐ°ŅĐ°Ņ ŅĐ˛ĐģŅĐĩŅŅŅ ŅĐŗŅĐžĐˇĐžĐš ĐąĐĩĐˇĐžĐŋĐ°ŅĐŊĐžŅŅĐ¸. ĐŅĐĩĐ´ĐŋĐžŅŅĐ¸ŅĐĩĐģŅĐŊĐž Đ˛ŅĐŋĐžĐģĐŊŅŅŅ"
            " ĐĩĐĩ Đ˛ <a href='tg://openmessage?user_id={}'>ĐĐˇĐąŅĐ°ĐŊĐŊŅŅ ŅĐžĐžĐąŅĐĩĐŊĐ¸ŅŅ</a>.</b>"
        ),
        "opening_tunnel": "đ <b>ĐŅĐēŅŅĐ˛Đ°Ņ ŅĐžĐŊĐŊĐĩĐģŅ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Netfoll...</b>",
        "tunnel_opened": (
            "đ <b>ĐĸĐžĐŊĐŊĐĩĐģŅ ĐžŅĐēŅŅŅ. Đ­ŅĐ° ŅŅŅĐģĐēĐ° ĐąŅĐ´ĐĩŅ Đ°ĐēŅĐ¸Đ˛ĐŊĐ° ĐŊĐĩ ĐąĐžĐģĐĩĐĩ ŅĐ°ŅĐ°</b>"
        ),
        "web_btn": "đ ĐĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ",
        "btn_yes": "đ¸ ĐŅĐĩ ŅĐ°Đ˛ĐŊĐž ĐžŅĐēŅŅŅŅ",
        "btn_no": "đģ ĐĐ°ĐēŅŅŅŅ",
        "lavhost_web": (
            "âī¸ <b>ĐĐž ŅŅĐžĐš ŅŅŅĐģĐēĐĩ ŅŅ ĐŋĐžĐŋĐ°Đ´ĐĩŅŅ Đ˛ Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ Netfoll ĐŊĐ°"
            " lavHost</b>\n\n<i>đĄ ĐĸĐĩĐąĐĩ ĐŊŅĐļĐŊĐž ĐąŅĐ´ĐĩŅ Đ°Đ˛ŅĐžŅĐ¸ĐˇĐžĐ˛Đ°ŅŅŅŅ, Đ¸ŅĐŋĐžĐģŅĐˇŅŅ Đ´Đ°ĐŊĐŊŅĐĩ,"
            " ŅĐēĐ°ĐˇĐ°ĐŊĐŊŅĐĩ ĐŋŅĐ¸ ĐŊĐ°ŅŅŅĐžĐšĐēĐĩ lavHost</i>"
        ),
        "disable_debugger": "â ĐŅĐģĐ°Đ´ŅĐ¸Đē Đ˛ĐēĐģŅŅĐĩĐŊ",
        "enable_debugger": "đĢ ĐŅĐģĐ°Đ´ŅĐ¸Đē Đ˛ŅĐēĐģŅŅĐĩĐŊ",
    }

    def get_watchers(self) -> tuple:
        return [
            str(watcher.__self__.__class__.strings["name"])
            for watcher in self.allmodules.watchers
            if watcher.__self__.__class__.strings is not None
        ], self._db.get(main.__name__, "disabled_watchers", {})

    async def _uninstall(self, call: InlineCall):
        await call.edit(self.strings("uninstall"))

        async with self._client.conversation("@BotFather") as conv:
            for msg in [
                "/deletebot",
                f"@{self.inline.bot_username}",
                "Yes, I am totally sure.",
            ]:
                await fw_protect()
                m = await conv.send_message(msg)
                r = await conv.get_response()

                logger.debug(">> %s", m.raw_text)
                logger.debug("<< %s", r.raw_text)

                await fw_protect()

                await m.delete()
                await r.delete()

        async for dialog in self._client.iter_dialogs(
            None,
            ignore_migrated=True,
        ):
            if (
                dialog.name
                in {
                    "netfoll-logs",
                    "netfoll-onload",
                    "netfoll-assets",
                    "netfoll-backups",
                    "netfoll-acc-switcher",
                    "silent-tags",
                }
                and dialog.is_channel
                and (
                    dialog.entity.participants_count == 1
                    or dialog.entity.participants_count == 2
                    and dialog.name in {"netfoll-logs", "silent-tags"}
                )
                or (
                    self._client.loader.inline.init_complete
                    and dialog.entity.id == self._client.loader.inline.bot_id
                )
            ):
                await fw_protect()
                await self._client.delete_dialog(dialog.entity)

                await fw_protect()

        folders = await self._client(GetDialogFiltersRequest())

        if any(folder.title == "netfoll" for folder in folders):
            folder_id = max(
                folders,
                key=lambda x: x.id,
            ).id
            await fw_protect()
            await self._client(UpdateDialogFilterRequest(id=folder_id))

        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.CRITICAL)

        await fw_protect()

        await self._client.log_out()

        restart()

    async def _uninstall_confirm_step_2(self, call: InlineCall):
        await call.edit(
            self.strings("deauth_confirm_step2"),
            utils.chunks(
                list(
                    sorted(
                        [
                            {
                                "text": self.strings("deauth_yes"),
                                "callback": self._uninstall,
                            },
                            *[
                                {
                                    "text": self.strings(f"deauth_no_{i}"),
                                    "action": "close",
                                }
                                for i in range(1, 4)
                            ],
                        ],
                        key=lambda _: random.random(),
                    )
                ),
                2,
            )
            + [
                [
                    {
                        "text": self.strings("deauth_cancel"),
                        "action": "close",
                    }
                ]
            ],
        )

    @loader.owner
    @loader.command(ru_doc="ĐŖĐ´Đ°ĐģĐ¸ŅŅ Netfoll")
    async def uninstall_netfoll(self, message: Message):
        """Uninstall Netfoll"""
        await self.inline.form(
            self.strings("deauth_confirm"),
            message,
            [
                {
                    "text": self.strings("deauth_confirm_btn"),
                    "callback": self._uninstall_confirm_step_2,
                },
                {"text": self.strings("deauth_cancel"), "action": "close"},
            ],
        )

    @loader.command(ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ°ĐēŅĐ¸Đ˛ĐŊŅĐĩ ŅĐŧĐžŅŅĐ¸ŅĐĩĐģĐ¸")
    async def watchers(self, message: Message):
        """List current watchers"""
        watchers, disabled_watchers = self.get_watchers()
        watchers = [
            f"âģī¸ {watcher}"
            for watcher in watchers
            if watcher not in list(disabled_watchers.keys())
        ]
        watchers += [f"đĸ {k} {v}" for k, v in disabled_watchers.items()]
        await utils.answer(
            message, self.strings("watchers").format("\n".join(watchers))
        )

    @loader.command(ru_doc="<module> - ĐĐēĐģŅŅĐ¸ŅŅ/Đ˛ŅĐēĐģŅŅĐ¸ŅŅ ŅĐŧĐžŅŅĐ¸ŅĐĩĐģŅ Đ˛ ŅĐĩĐēŅŅĐĩĐŧ ŅĐ°ŅĐĩ")
    async def watcherbl(self, message: Message):
        """<module> - Toggle watcher in current chat"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args"))
            return

        watchers, disabled_watchers = self.get_watchers()

        if args.lower() not in map(lambda x: x.lower(), watchers):
            await utils.answer(message, self.strings("mod404").format(args))
            return

        args = next((x.lower() == args.lower() for x in watchers), False)

        current_bl = [
            v for k, v in disabled_watchers.items() if k.lower() == args.lower()
        ]
        current_bl = current_bl[0] if current_bl else []

        chat = utils.get_chat_id(message)
        if chat not in current_bl:
            if args in disabled_watchers:
                for k in disabled_watchers:
                    if k.lower() == args.lower():
                        disabled_watchers[k].append(chat)
                        break
            else:
                disabled_watchers[args] = [chat]

            await utils.answer(
                message,
                self.strings("disabled").format(args) + " <b>in current chat</b>",
            )
        else:
            for k in disabled_watchers.copy():
                if k.lower() == args.lower():
                    disabled_watchers[k].remove(chat)
                    if not disabled_watchers[k]:
                        del disabled_watchers[k]
                    break

            await utils.answer(
                message,
                self.strings("enabled").format(args) + " <b>in current chat</b>",
            )

        self._db.set(main.__name__, "disabled_watchers", disabled_watchers)

    @loader.command(
        ru_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> - ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŗĐģĐžĐąĐ°ĐģŅĐŊŅĐŧĐ¸ ĐŋŅĐ°Đ˛Đ¸ĐģĐ°ĐŧĐ¸ ŅĐŧĐžŅŅĐ¸ŅĐĩĐģŅ\n"
            "ĐŅĐŗŅĐŧĐĩĐŊŅŅ:\n"
            "[-c - ŅĐžĐģŅĐēĐž Đ˛ ŅĐ°ŅĐ°Ņ]\n"
            "[-p - ŅĐžĐģŅĐēĐž Đ˛ ĐģŅ]\n"
            "[-o - ŅĐžĐģŅĐēĐž Đ¸ŅŅĐžĐ´ŅŅĐ¸Đĩ]\n"
            "[-i - ŅĐžĐģŅĐēĐž Đ˛ŅĐžĐ´ŅŅĐ¸Đĩ]"
        )
    )
    async def watchercmd(self, message: Message):
        """<module> - Toggle global watcher rules
        Args:
        [-c - only in chats]
        [-p - only in pm]
        [-o - only out]
        [-i - only incoming]"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("args"))

        chats, pm, out, incoming = False, False, False, False

        if "-c" in args:
            args = args.replace("-c", "").replace("  ", " ").strip()
            chats = True

        if "-p" in args:
            args = args.replace("-p", "").replace("  ", " ").strip()
            pm = True

        if "-o" in args:
            args = args.replace("-o", "").replace("  ", " ").strip()
            out = True

        if "-i" in args:
            args = args.replace("-i", "").replace("  ", " ").strip()
            incoming = True

        if chats and pm:
            pm = False
        if out and incoming:
            incoming = False

        watchers, disabled_watchers = self.get_watchers()

        if args.lower() not in [watcher.lower() for watcher in watchers]:
            return await utils.answer(message, self.strings("mod404").format(args))

        args = [watcher for watcher in watchers if watcher.lower() == args.lower()][0]

        if chats or pm or out or incoming:
            disabled_watchers[args] = [
                *(["only_chats"] if chats else []),
                *(["only_pm"] if pm else []),
                *(["out"] if out else []),
                *(["in"] if incoming else []),
            ]
            self._db.set(main.__name__, "disabled_watchers", disabled_watchers)
            await utils.answer(
                message,
                self.strings("enabled").format(args)
                + f" (<code>{disabled_watchers[args]}</code>)",
            )
            return

        if args in disabled_watchers and "*" in disabled_watchers[args]:
            await utils.answer(message, self.strings("enabled").format(args))
            del disabled_watchers[args]
            self._db.set(main.__name__, "disabled_watchers", disabled_watchers)
            return

        disabled_watchers[args] = ["*"]
        self._db.set(main.__name__, "disabled_watchers", disabled_watchers)
        await utils.answer(message, self.strings("disabled").format(args))

    @loader.command(ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ NoNick Đ´ĐģŅ ĐžĐŋŅĐĩĐ´ĐĩĐģĐĩĐŊĐŊĐžĐŗĐž ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ")
    async def nonickuser(self, message: Message):
        """Allow no nickname for certain user"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("reply_required"))
            return

        u = reply.sender_id
        if not isinstance(u, int):
            u = u.user_id

        nn = self._db.get(main.__name__, "nonickusers", [])
        if u not in nn:
            nn += [u]
            nn = list(set(nn))  # skipcq: PTC-W0018
            await utils.answer(message, self.strings("user_nn").format("on"))
        else:
            nn = list(set(nn) - {u})
            await utils.answer(message, self.strings("user_nn").format("off"))

        self._db.set(main.__name__, "nonickusers", nn)

    @loader.command(ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ NoNick Đ´ĐģŅ ĐžĐŋŅĐĩĐ´ĐĩĐģĐĩĐŊĐŊĐžĐŗĐž ŅĐ°ŅĐ°")
    async def nonickchat(self, message: Message):
        """Allow no nickname in certain chat"""
        if message.is_private:
            await utils.answer(message, self.strings("private_not_allowed"))
            return

        chat = utils.get_chat_id(message)

        nn = self._db.get(main.__name__, "nonickchats", [])
        if chat not in nn:
            nn += [chat]
            nn = list(set(nn))  # skipcq: PTC-W0018
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    utils.escape_html((await message.get_chat()).title),
                    "on",
                ),
            )
        else:
            nn = list(set(nn) - {chat})
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    utils.escape_html((await message.get_chat()).title),
                    "off",
                ),
            )

        self._db.set(main.__name__, "nonickchats", nn)

    @loader.command(ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ NoNick Đ´ĐģŅ ĐžĐŋŅĐĩĐ´ĐĩĐģĐĩĐŊĐŊĐžĐš ĐēĐžĐŧĐ°ĐŊĐ´Ņ")
    async def nonickcmdcmd(self, message: Message):
        """Allow certain command to be executed without nickname"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_cmd"))
            return

        if args not in self.allmodules.commands:
            await utils.answer(message, self.strings("cmd404"))
            return

        nn = self._db.get(main.__name__, "nonickcmds", [])
        if args not in nn:
            nn += [args]
            nn = list(set(nn))
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    self.get_prefix() + args,
                    "on",
                ),
            )
        else:
            nn = list(set(nn) - {args})
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    self.get_prefix() + args,
                    "off",
                ),
            )

        self._db.set(main.__name__, "nonickcmds", nn)

    @loader.command(ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐēŅĐ¸Đ˛ĐŊŅŅ NoNick ĐēĐžĐŧĐ°ĐŊĐ´",)
    async def nonickcmds(self, message: Message):
        """Returns the list of NoNick commands"""
        if not self._db.get(main.__name__, "nonickcmds", []):
            await utils.answer(message, self.strings("nothing"))
            return

        await utils.answer(
            message,
            self.strings("cmd_nn_list").format(
                "\n".join(
                    [
                        f"âĢī¸ <code>{self.get_prefix()}{cmd}</code>"
                        for cmd in self._db.get(main.__name__, "nonickcmds", [])
                    ]
                )
            ),
        )

    @loader.command(ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐēŅĐ¸Đ˛ĐŊŅŅ NoNick ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģĐĩĐš",)
    async def nonickusers(self, message: Message):
        """Returns the list of NoNick users"""
        users = []
        for user_id in self._db.get(main.__name__, "nonickusers", []).copy():
            try:
                user = await self._client.get_entity(user_id)
            except Exception:
                self._db.set(
                    main.__name__,
                    "nonickusers",
                    list(
                        (
                            set(self._db.get(main.__name__, "nonickusers", []))
                            - {user_id}
                        )
                    ),
                )

                logger.warning("User %s removed from nonickusers list", user_id)
                continue

            users += [
                'âĢī¸ <b><a href="tg://user?id={}">{}</a></b>'.format(
                    user_id,
                    utils.escape_html(get_display_name(user)),
                )
            ]

        if not users:
            await utils.answer(message, self.strings("nothing"))
            return

        await utils.answer(
            message,
            self.strings("user_nn_list").format("\n".join(users)),
        )

    @loader.command(ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐēŅĐ¸Đ˛ĐŊŅŅ NoNick ŅĐ°ŅĐžĐ˛")
    async def nonickchats(self, message: Message):
        """Returns the list of NoNick chats"""
        chats = []
        for chat in self._db.get(main.__name__, "nonickchats", []):
            try:
                chat_entity = await self._client.get_entity(int(chat))
            except Exception:
                self._db.set(
                    main.__name__,
                    "nonickchats",
                    list(
                        (set(self._db.get(main.__name__, "nonickchats", [])) - {chat})
                    ),
                )

                logger.warning("Chat %s removed from nonickchats list", chat)
                continue

            chats += [
                'âĢī¸ <b><a href="{}">{}</a></b>'.format(
                    utils.get_entity_url(chat_entity),
                    utils.escape_html(get_display_name(chat_entity)),
                )
            ]

        if not chats:
            await utils.answer(message, self.strings("nothing"))
            return

        await utils.answer(
            message,
            self.strings("user_nn_list").format("\n".join(chats)),
        )

    async def inline__setting(self, call: InlineCall, key: str, state: bool = False):
        if callable(key):
            key()
            telethon.extensions.html.CUSTOM_EMOJIS = not main.get_config_key(
                "disable_custom_emojis"
            )
        else:
            self._db.set(main.__name__, key, state)

        if key == "no_nickname" and state and self.get_prefix() == ".":
            await call.answer(
                self.strings("nonick_warning"),
                show_alert=True,
            )
        else:
            await call.answer("Configuration value saved!")

        await call.edit(
            self.strings("inline_settings"),
            reply_markup=self._get_settings_markup(),
        )

    async def inline__update(
        self,
        call: InlineCall,
        confirm_required: bool = False,
    ):
        if confirm_required:
            await call.edit(
                self.strings("confirm_update"),
                reply_markup=[
                    {"text": "đĒ Update", "callback": self.inline__update},
                    {"text": "đĢ Cancel", "action": "close"},
                ],
            )
            return

        await call.answer("You userbot is being updated...", show_alert=True)
        await call.delete()
        await self.invoke("update", "-f", peer="me")

    async def inline__restart(
        self,
        call: InlineCall,
        confirm_required: bool = False,
    ):
        if confirm_required:
            await call.edit(
                self.strings("confirm_restart"),
                reply_markup=[
                    {"text": "đ Restart", "callback": self.inline__restart},
                    {"text": "đĢ Cancel", "action": "close"},
                ],
            )
            return

        await call.answer("You userbot is being restarted...", show_alert=True)
        await call.delete()
        await self.invoke("restart", "-f", peer="me")

    def _get_settings_markup(self) -> list:
        return [
            [
                (
                    {
                        "text": "â NoNick",
                        "callback": self.inline__setting,
                        "args": (
                            "no_nickname",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "no_nickname", False)
                    else {
                        "text": "đĢ NoNick",
                        "callback": self.inline__setting,
                        "args": (
                            "no_nickname",
                            True,
                        ),
                    }
                ),
                (
                    {
                        "text": "â Grep",
                        "callback": self.inline__setting,
                        "args": (
                            "grep",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "grep", False)
                    else {
                        "text": "đĢ Grep",
                        "callback": self.inline__setting,
                        "args": (
                            "grep",
                            True,
                        ),
                    }
                ),
                (
                    {
                        "text": "â InlineLogs",
                        "callback": self.inline__setting,
                        "args": (
                            "inlinelogs",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "inlinelogs", True)
                    else {
                        "text": "đĢ InlineLogs",
                        "callback": self.inline__setting,
                        "args": (
                            "inlinelogs",
                            True,
                        ),
                    }
                ),
            ],
            [
                {
                    "text": self.strings("do_not_suggest_fs"),
                    "callback": self.inline__setting,
                    "args": (
                        "disable_modules_fs",
                        False,
                    ),
                }
                if self._db.get(main.__name__, "disable_modules_fs", False)
                else {
                    "text": self.strings("suggest_fs"),
                    "callback": self.inline__setting,
                    "args": (
                        "disable_modules_fs",
                        True,
                    ),
                }
            ],
            [
                (
                    {
                        "text": self.strings("use_fs"),
                        "callback": self.inline__setting,
                        "args": (
                            "permanent_modules_fs",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "permanent_modules_fs", False)
                    else {
                        "text": self.strings("do_not_use_fs"),
                        "callback": self.inline__setting,
                        "args": (
                            "permanent_modules_fs",
                            True,
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("suggest_subscribe"),
                        "callback": self.inline__setting,
                        "args": (
                            "suggest_subscribe",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "suggest_subscribe", True)
                    else {
                        "text": self.strings("do_not_suggest_subscribe"),
                        "callback": self.inline__setting,
                        "args": (
                            "suggest_subscribe",
                            True,
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("no_custom_emojis"),
                        "callback": self.inline__setting,
                        "args": (
                            lambda: main.save_config_key(
                                "disable_custom_emojis", False
                            ),
                        ),
                    }
                    if main.get_config_key("disable_custom_emojis")
                    else {
                        "text": self.strings("custom_emojis"),
                        "callback": self.inline__setting,
                        "args": (
                            lambda: main.save_config_key("disable_custom_emojis", True),
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("disable_debugger"),
                        "callback": self.inline__setting,
                        "args": (lambda: self._db.set(log.__name__, "debugger", False)),
                    }
                    if self._db.get(log.__name__, "debugger", False)
                    else {
                        "text": self.strings("enable_debugger"),
                        "callback": self.inline__setting,
                        "args": (lambda: self._db.set(log.__name__, "debugger", True),),
                    }
                ),
            ],
            [
                {
                    "text": self.strings("btn_restart"),
                    "callback": self.inline__restart,
                    "args": (True,),
                },
                {
                    "text": self.strings("btn_update"),
                    "callback": self.inline__update,
                    "args": (True,),
                },
            ],
            [{"text": self.strings("close_menu"), "action": "close"}],
        ]

    @loader.owner
    @loader.command(ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸")
    async def settings(self, message: Message):
        """Show settings menu"""
        await self.inline.form(
            self.strings("inline_settings"),
            message=message,
            reply_markup=self._get_settings_markup(),
        )

    @loader.owner
    @loader.command(ru_doc="ĐŅĐēŅŅŅŅ ŅĐžĐŊĐŊĐĩĐģŅ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Netfoll")
    async def weburl(self, message: Message, force: bool = False):
        """Opens web tunnel to your Netfoll web interface"""
        if "LAVHOST" in os.environ:
            form = await self.inline.form(
                self.strings("lavhost_web"),
                message=message,
                reply_markup={
                    "text": self.strings("web_btn"),
                    "url": await main.hikka.web.get_url(proxy_pass=False),
                },
                gif="https://t.me/hikari_assets/28",
            )
            return

        if (
            not force
            and not message.is_private
            and "force_insecure" not in message.raw_text.lower()
        ):
            try:
                if not await self.inline.form(
                    self.strings("privacy_leak_nowarn").format(self._client.tg_id),
                    message=message,
                    reply_markup=[
                        {
                            "text": self.strings("btn_yes"),
                            "callback": self.weburl,
                            "args": (True,),
                        },
                        {"text": self.strings("btn_no"), "action": "close"},
                    ],
                    gif="https://i.gifer.com/embedded/download/Z5tS.gif",
                ):
                    raise Exception
            except Exception:
                await utils.answer(
                    message,
                    self.strings("privacy_leak").format(
                        self._client.tg_id,
                        self.get_prefix(),
                    ),
                )

            return

        if force:
            form = message
            await form.edit(
                self.strings("opening_tunnel"),
                reply_markup={"text": "đ Wait...", "data": "empty"},
                gif=(
                    "https://i.gifer.com/origin/e4/e43e1b221fd960003dc27d2f2f1b8ce1.gif"
                ),
            )
        else:
            form = await self.inline.form(
                self.strings("opening_tunnel"),
                message=message,
                reply_markup={"text": "đ Wait...", "data": "empty"},
                gif=(
                    "https://i.gifer.com/origin/e4/e43e1b221fd960003dc27d2f2f1b8ce1.gif"
                ),
            )

        url = await main.hikka.web.get_url(proxy_pass=True)

        await form.edit(
            self.strings("tunnel_opened"),
            reply_markup={"text": self.strings("web_btn"), "url": url},
            gif="https://t.me/hikari_assets/48",
        )

    @loader.loop(interval=1, autostart=True)
    async def loop(self):
        obj = self.allmodules.get_approved_channel
        if not obj:
            return

        channel, event = obj

        try:
            await self._client(JoinChannelRequest(channel))
        except Exception:
            logger.exception("Failed to join channel")
            event.status = False
            event.set()
        else:
            event.status = True
            event.set()

    def _get_all_IDM(self, module: str):
        return {
            getattr(getattr(self.lookup(module), name), "name", name): getattr(
                self.lookup(module), name
            )
            for name in dir(self.lookup(module))
            if getattr(getattr(self.lookup(module), name), "is_debug_method", False)
        }

    @loader.command()
    async def invokecmd(self, message: Message):
        """<module or `core` for built-in methods> <method> - Only for debugging purposes. DO NOT USE IF YOU'RE NOT A DEVELOPER
        """
        args = utils.get_args_raw(message)
        if not args or len(args.split()) < 2:
            await utils.answer(message, self.strings("no_args"))
            return

        module = args.split()[0]
        method = args.split(maxsplit=1)[1]

        if module != "core" and not self.lookup(module):
            await utils.answer(message, self.strings("module404").format(module))
            return

        if (
            module == "core"
            and method not in ALL_INVOKES
            or module != "core"
            and method not in self._get_all_IDM(module)
        ):
            await utils.answer(message, self.strings("invoke404").format(method))
            return

        message = await utils.answer(
            message, self.strings("invoking").format(method, module)
        )
        result = ""

        if module == "core":
            if method == "clear_entity_cache":
                result = (
                    f"Dropped {len(self._client._hikka_entity_cache)} cache records"
                )
                self._client._hikka_entity_cache = {}
            elif method == "clear_fulluser_cache":
                result = (
                    f"Dropped {len(self._client._hikka_fulluser_cache)} cache records"
                )
                self._client._hikka_fulluser_cache = {}
            elif method == "clear_fullchannel_cache":
                result = (
                    f"Dropped {len(self._client._hikka_fullchannel_cache)} cache"
                    " records"
                )
                self._client._hikka_fullchannel_cache = {}
            elif method == "clear_perms_cache":
                result = f"Dropped {len(self._client._hikka_perms_cache)} cache records"
                self._client._hikka_perms_cache = {}
            elif method == "clear_cache":
                result = (
                    f"Dropped {len(self._client._hikka_entity_cache)} entity cache"
                    " records\nDropped"
                    f" {len(self._client._hikka_fulluser_cache)} fulluser cache"
                    " records\nDropped"
                    f" {len(self._client._hikka_fullchannel_cache)} fullchannel cache"
                    " records"
                )
                self._client._hikka_entity_cache = {}
                self._client._hikka_fulluser_cache = {}
                self._client._hikka_fullchannel_cache = {}
                self._client.hikka_me = await self._client.get_me()
            elif method == "reload_core":
                core_quantity = await self.lookup("loader").reload_core()
                result = f"Reloaded {core_quantity} core modules"
            elif method == "inspect_cache":
                result = (
                    "Entity cache:"
                    f" {len(self._client._hikka_entity_cache)} records\nFulluser cache:"
                    f" {len(self._client._hikka_fulluser_cache)} records\nFullchannel"
                    f" cache: {len(self._client._hikka_fullchannel_cache)} records"
                )
            elif method == "inspect_modules":
                result = (
                    "Loaded modules: {}\nLoaded core modules: {}\nLoaded user"
                    " modules: {}"
                ).format(
                    len(self.allmodules.modules),
                    sum(
                        module.__origin__.startswith("<core")
                        for module in self.allmodules.modules
                    ),
                    sum(
                        not module.__origin__.startswith("<core")
                        for module in self.allmodules.modules
                    ),
                )
        else:
            result = await self._get_all_IDM(module)[method](message)

        await utils.answer(
            message,
            self.strings("invoke").format(method, utils.escape_html(result)),
        )
