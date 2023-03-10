# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# đ https://github.com/MXRRI/Netfoll

import ast
import contextlib
import functools
import typing
from math import ceil

from telethon.tl.types import Message

from .. import loader, translations, utils
from ..inline.types import InlineCall

# Everywhere in this module, we use the following naming convention:
# `obj_type` of non-core module = False
# `obj_type` of core module = True
# `obj_type` of library = "library"


@loader.tds
class NetfollConfigMod(loader.Module):
    """Interactive configurator for Netfoll Userbot"""

    strings = {
        "name": "NetfollConfig",
        "choose_core": "âī¸ <b>Choose a category</b>",
        "configure": "âī¸ <b>Choose a module to configure</b>",
        "configure_lib": "đĻ <b>Choose a library to configure</b>",
        "configuring_mod": (
            "âī¸ <b>Choose config option for mod</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>Choose config option for library</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>Configuring option</b> <code>{}</code> <b>of mod"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>Configuring option</b> <code>{}</code> <b>of library"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>Option"
            "</b> <code>{}</code> <b>of module</b> <code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>Option"
            "</b> <code>{}</code> <b>of library</b> <code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Option</b> <code>{}</code> <b>of module</b> <code>{}</code> <b>has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Option</b> <code>{}</code> <b>of library</b> <code>{}</code> <b>has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "args": "đĢ <b>You specified incorrect args</b>",
        "no_mod": "đĢ <b>Module doesn't exist</b>",
        "no_option": "đĢ <b>Configuration option doesn't exist</b>",
        "validation_error": "đĢ <b>You entered incorrect config value.\nError: {}</b>",
        "try_again": "đ Try again",
        "typehint": "đĩī¸ <b>Must be a{eng_art} {}</b>",
        "set": "set",
        "set_default_btn": "âģī¸ Reset default",
        "enter_value_btn": "âī¸ Enter value",
        "enter_value_desc": "âī¸ Enter new configuration value for this option",
        "add_item_desc": "âī¸ Enter item to add",
        "remove_item_desc": "âī¸ Enter item to remove",
        "back_btn": "đ Back",
        "close_btn": "âī¸ Close",
        "add_item_btn": "â Add item",
        "remove_item_btn": "â Remove item",
        "show_hidden": "đ¸ Show value",
        "hide_value": "đ Hide value",
        "builtin": "đž Built-in",
        "external": "â External",
        "libraries": "đĻ Libraries",
    }

    strings_ru = {
        "choose_core": "âī¸ <b>ĐŅĐąĐĩŅĐ¸ ĐēĐ°ŅĐĩĐŗĐžŅĐ¸Ņ</b>",
        "configure": "âī¸ <b>ĐŅĐąĐĩŅĐ¸ ĐŧĐžĐ´ŅĐģŅ Đ´ĐģŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸</b>",
        "configure_lib": "đĻ <b>ĐŅĐąĐĩŅĐ¸ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēŅ Đ´ĐģŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸</b>",
        "configuring_mod": (
            "âī¸ <b>ĐŅĐąŅĐ°ĐŊ ĐŧĐžĐ´ŅĐģŅ:</b> <code>{}</code>\n\n<b>ĐĸĐĩĐēŅŅĐ¸Đĩ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>ĐŅĐąĐĩŅĐ¸ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code>\n\n<b>ĐĸĐĩĐēŅŅĐ¸Đĩ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ŅĐžŅŅĐ°ĐŊĐĩĐŊ!</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code><b>"
            " ŅĐžŅŅĐ°ĐŊĐĩĐŊ!</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "_cls_doc": "ĐĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ĐŊŅĐš ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐžŅ Netfoll",
        "args": "đĢ <b>ĐĸŅ ŅĐēĐ°ĐˇĐ°Đģ ĐŊĐĩĐ˛ĐĩŅĐŊŅĐĩ Đ°ŅĐŗŅĐŧĐĩĐŊŅŅ</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>",
        "no_option": "đĢ <b>ĐŖ ĐŧĐžĐ´ŅĐģŅ ĐŊĐĩŅ ŅĐ°ĐēĐžĐŗĐž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐēĐžĐŊŅĐ¸ĐŗĐ°</b>",
        "validation_error": (
            "đĢ <b>ĐĐ˛ĐĩĐ´ĐĩĐŊĐž ĐŊĐĩĐēĐžŅŅĐĩĐēŅĐŊĐžĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐēĐžĐŊŅĐ¸ĐŗĐ°.\nĐŅĐ¸ĐąĐēĐ°: {}</b>"
        ),
        "try_again": "đ ĐĐžĐŋŅĐžĐąĐžĐ˛Đ°ŅŅ ĐĩŅĐĩ ŅĐ°Đˇ",
        "typehint": "đĩī¸ <b>ĐĐžĐģĐļĐŊĐž ĐąŅŅŅ {}</b>",
        "set": "ĐŋĐžŅŅĐ°Đ˛Đ¸ŅŅ",
        "set_default_btn": "âģī¸ ĐĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ",
        "enter_value_btn": "âī¸ ĐĐ˛ĐĩŅŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "enter_value_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐŊĐžĐ˛ĐžĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ŅŅĐžĐŗĐž ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°",
        "add_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ŅĐģĐĩĐŧĐĩĐŊŅ, ĐēĐžŅĐžŅŅĐš ĐŊŅĐļĐŊĐž Đ´ĐžĐąĐ°Đ˛Đ¸ŅŅ",
        "remove_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ŅĐģĐĩĐŧĐĩĐŊŅ, ĐēĐžŅĐžŅŅĐš ĐŊŅĐļĐŊĐž ŅĐ´Đ°ĐģĐ¸ŅŅ",
        "back_btn": "đ ĐĐ°ĐˇĐ°Đ´",
        "close_btn": "âī¸ ĐĐ°ĐēŅŅŅŅ",
        "add_item_btn": "â ĐĐžĐąĐ°Đ˛Đ¸ŅŅ",
        "remove_item_btn": "â ĐŖĐ´Đ°ĐģĐ¸ŅŅ",
        "show_hidden": "đ¸ ĐĐžĐēĐ°ĐˇĐ°ŅŅ",
        "hide_value": "đ ĐĄĐēŅŅŅŅ",
        "builtin": "đž ĐŅŅŅĐžĐĩĐŊĐŊŅĐĩ",
        "external": "â ĐŖŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊĐŊŅĐĩ",
        "libraries": "đĻ ĐĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸",
    }

    strings_uk = {
        "choose_core": "âī¸ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐēĐ°ŅĐĩĐŗĐžŅŅŅ</b>",
        "configure": "âī¸ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐŧĐžĐ´ŅĐģŅ Đ´ĐģŅ ĐēĐžĐŊŅŅĐŗŅŅĐ°ŅŅŅ</b>",
        "configure_lib": "đĻ <b>ĐĐ¸ĐąĐĩŅŅŅŅ ĐąŅĐąĐģŅĐžŅĐĩĐēŅ Đ´ĐģŅ ĐŊĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊŅ</b>",
        "configuring_mod": (
            "âī¸ <b>ĐĐ¸ĐąĐ¸ŅĐ°ŅŅŅŅŅ ĐŧĐžĐ´ŅĐģŅ:</b> <code>{}</code>\n\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš"
            " ĐĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊĐŊŅ:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>ĐŅĐąĐĩŅĐ¸ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code>\n\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš"
            " ĐĐ°ĐģĐ°ŅŅŅĐ˛Đ°ĐŊĐŊŅ:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ĐŖĐŋŅĐ°Đ˛ĐģŅĐŊĐŊŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>ĐŖĐŋŅĐ°Đ˛ĐģŅĐŊĐŊŅ ĐĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ</b> <code>{}</code> <b>ĐąŅĐąĐģŅĐžŅĐĩĐēĐ°"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ĐˇĐąĐĩŅĐĩĐļĐĩĐŊĐž!</b>\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐąŅĐąĐģŅĐžŅĐĩĐēĐ¸</b> <code>{}</code><b>"
            " ĐˇĐąĐĩŅĐĩĐļĐĩĐŊĐž!</b>\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ŅĐēĐ¸ĐŊŅŅĐž Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐˇĐ° ĐˇĐ°ĐŧĐžĐ˛ŅŅĐ˛Đ°ĐŊĐŊŅĐŧ</b>\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐąŅĐąĐģŅĐžŅĐĩĐēĐ¸</b> <code>{}</code><b>"
            " ŅĐēĐ¸ĐŊŅŅĐž Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐˇĐ° ĐˇĐ°ĐŧĐžĐ˛ŅŅĐ˛Đ°ĐŊĐŊŅĐŧ</b>\n<b>ĐĐžŅĐžŅĐŊĐ¸Đš: {}</b>"
        ),
        "_cls_doc": "ĐĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ĐŊĐ¸Đš ĐēĐžĐŊŅŅĐŗŅŅĐ°ŅĐžŅ Netfoll",
        "args": "đĢ <b>ĐĸĐ¸ Đ˛ĐēĐ°ĐˇĐ°Đ˛ ĐŊĐĩĐ˛ŅŅĐŊŅ Đ°ŅĐŗŅĐŧĐĩĐŊŅĐ¸</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ŅŅĐŊŅŅ</b>",
        "no_option": "đĢ <b>ĐŖ ĐŧĐžĐ´ŅĐģŅ ĐŊĐĩĐŧĐ°Ņ ŅĐ°ĐēĐžĐŗĐž ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐēĐžĐŊŅŅĐŗĐ°</b>",
        "validation_error": (
            "đĢ <b>ĐĐ˛ĐĩĐ´ĐĩĐŊĐž ĐŊĐĩĐēĐžŅĐĩĐēŅĐŊĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ĐēĐžĐŊŅŅĐŗĐ°.\ĐĐžĐŧĐ¸ĐģĐēĐ°: {}</b>"
        ),
        "try_again": "đ ĐĄĐŋŅĐžĐąŅĐ˛Đ°ŅĐ¸ ŅĐĩ ŅĐ°Đˇ",
        "typehint": "đĩī¸ <b>ĐĐ°Ņ ĐąŅŅĐ¸ {}</b>",
        "set": "ĐŋĐžŅŅĐ°Đ˛Đ¸ŅŅ",
        "set_default_btn": "âģī¸ ĐĐŊĐ°ŅĐĩĐŊĐŊŅ ĐˇĐ° ĐˇĐ°ĐŧĐžĐ˛ŅŅĐ˛Đ°ĐŊĐŊŅĐŧ",
        "enter_value_btn": "âī¸ ĐĐ˛ĐĩŅŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ  ",
        "enter_value_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐŊĐžĐ˛Đĩ ĐˇĐŊĐ°ŅĐĩĐŊĐŊŅ ŅŅĐžĐŗĐž ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°",
        "add_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐĩĐģĐĩĐŧĐĩĐŊŅ, ŅĐēĐ¸Đš ĐŋĐžŅŅŅĐąĐŊĐž Đ´ĐžĐ´Đ°ŅĐ¸",
        "remove_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐĩĐģĐĩĐŧĐĩĐŊŅ, ŅĐēĐ¸Đš ĐŋĐžŅŅŅĐąĐŊĐž Đ˛Đ¸Đ´Đ°ĐģĐ¸ŅĐ¸",
        "back_btn": "đ ĐĐ°ĐˇĐ°Đ´",
        "close_btn": "âī¸ ĐĐ°ĐŋĐģŅŅĐ¸ŅĐ¸",
        "add_item_btn": "â ĐĐžĐ´Đ°Đ˛ŅĐ¸",
        "remove_item_btn": "â ĐĐ¸Đ´Đ°ĐģĐ¸ŅĐ¸",
        "show_hidden": "đ¸ ĐĐžĐēĐ°ĐˇĐ°Đ˛ŅĐ¸",
        "hide_value": "đ ĐĄŅĐžĐ˛Đ°Đ˛ŅĐ¸",
        "builtin": "đž ĐŖĐąŅĐ´ĐžĐ˛Đ°ĐŊĐ¸Đš",
        "external": "â ĐŖŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đš",
        "libraries": "đĻ ĐŅĐąĐģŅĐžŅĐĩĐēĐ¸",
    }

    _row_size = 3
    _num_rows = 5

    @staticmethod
    def prep_value(value: typing.Any) -> typing.Any:
        if isinstance(value, str):
            return f"</b><code>{utils.escape_html(value.strip())}</code><b>"

        if isinstance(value, list) and value:
            return (
                "</b><code>[</code>\n    "
                + "\n    ".join(
                    [f"<code>{utils.escape_html(str(item))}</code>" for item in value]
                )
                + "\n<code>]</code><b>"
            )

        return f"</b><code>{utils.escape_html(value)}</code><b>"

    def hide_value(self, value: typing.Any) -> str:
        if isinstance(value, list) and value:
            return self.prep_value(["*" * len(str(i)) for i in value])

        return self.prep_value("*" * len(str(value)))

    def _get_value(self, mod: str, option: str) -> str:
        return (
            self.prep_value(self.lookup(mod).config[option])
            if (
                not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
            )
            else self.hide_value(self.lookup(mod).config[option])
        )

    async def inline__set_config(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__reset_default(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        mod_instance = self.lookup(mod)
        mod_instance.config[option] = mod_instance.config.getdef(option)

        await call.edit(
            self.strings(
                "option_reset" if isinstance(obj_type, bool) else "option_reset_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__set_bool(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        validator = self.lookup(mod).config._config[option].validator
        doc = utils.escape_html(
            next(
                (
                    validator.doc[lang]
                    for lang in self._db.get(translations.__name__, "lang", "en").split(
                        " "
                    )
                    if lang in validator.doc
                ),
                validator.doc["en"],
            )
        )

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                utils.escape_html(self.lookup(mod).config.getdoc(option)),
                self.prep_value(self.lookup(mod).config.getdef(option)),
                self.prep_value(self.lookup(mod).config[option])
                if not validator or validator.internal_id != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
                if doc
                else "",
            ),
            reply_markup=self._generate_bool_markup(mod, option, obj_type),
        )

        await call.answer("â")

    def _generate_bool_markup(
        self,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                *(
                    [
                        {
                            "text": f"â {self.strings('set')} `False`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    else [
                        {
                            "text": f"â {self.strings('set')} `True`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                )
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__add_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            with contextlib.suppress(Exception):
                query = ast.literal_eval(query)

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            self.lookup(mod).config[option] = self.lookup(mod).config[option] + query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__remove_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            with contextlib.suppress(Exception):
                query = ast.literal_eval(query)

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            query = list(map(str, query))

            old_config_len = len(self.lookup(mod).config[option])

            self.lookup(mod).config[option] = [
                i for i in self.lookup(mod).config[option] if str(i) not in query
            ]

            if old_config_len == len(self.lookup(mod).config[option]):
                raise loader.validators.ValidationError(
                    f"Nothing from passed value ({self.prep_value(query)}) is not in"
                    " target list"
                )
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    def _generate_series_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("remove_item_btn"),
                            "input": self.strings("remove_item_desc"),
                            "handler": self.inline__remove_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                        {
                            "text": self.strings("add_item_btn"),
                            "input": self.strings("add_item_desc"),
                            "handler": self.inline__add_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                    ]
                    if self.lookup(mod).config[option]
                    else []
                ),
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def _choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

        await call.answer("â")

    async def _multi_choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            if value in self.lookup(mod).config._config[option].value:
                self.lookup(mod).config._config[option].value.remove(value)
            else:
                self.lookup(mod).config._config[option].value += [value]

            self.lookup(mod).config.reload()
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await self.inline__configure_option(call, mod, option, False, obj_type)
        await call.answer("â")

    def _generate_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'âī¸' if self.lookup(mod).config[option] == value else 'đ'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : 6
                if self.lookup(mod).config[option]
                != self.lookup(mod).config.getdef(option)
                else 7
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    def _generate_multi_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'âī¸' if value in self.lookup(mod).config[option] else 'âģī¸'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._multi_choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : 6
                if self.lookup(mod).config[option]
                != self.lookup(mod).config.getdef(option)
                else 7
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__configure_option(
        self,
        call: InlineCall,
        mod: str,
        config_opt: str,
        force_hidden: bool = False,
        obj_type: typing.Union[bool, str] = False,
    ):
        module = self.lookup(mod)
        args = [
            utils.escape_html(config_opt),
            utils.escape_html(mod),
            utils.escape_html(module.config.getdoc(config_opt)),
            self.prep_value(module.config.getdef(config_opt)),
            self.prep_value(module.config[config_opt])
            if not module.config._config[config_opt].validator
            or module.config._config[config_opt].validator.internal_id != "Hidden"
            or force_hidden
            else self.hide_value(module.config[config_opt]),
        ]

        if (
            module.config._config[config_opt].validator
            and module.config._config[config_opt].validator.internal_id == "Hidden"
        ):
            additonal_button_row = (
                [
                    [
                        {
                            "text": self.strings("hide_value"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
                if force_hidden
                else [
                    [
                        {
                            "text": self.strings("show_hidden"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
            )
        else:
            additonal_button_row = []

        try:
            validator = module.config._config[config_opt].validator
            doc = utils.escape_html(
                next(
                    (
                        validator.doc[lang]
                        for lang in self._db.get(
                            translations.__name__, "lang", "en"
                        ).split(" ")
                        if lang in validator.doc
                    ),
                    validator.doc["en"],
                )
            )
        except Exception:
            doc = None
            validator = None
            args += [""]
        else:
            args += [
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
            ]
            if validator.internal_id == "Boolean":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_bool_markup(mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Series":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_series_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Choice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_choice_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "MultiChoice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_multi_choice_markup(
                        call, mod, config_opt, obj_type
                    ),
                )
                return

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(*args),
            reply_markup=additonal_button_row
            + [
                [
                    {
                        "text": self.strings("enter_value_btn"),
                        "input": self.strings("enter_value_desc"),
                        "handler": self.inline__set_config,
                        "args": (mod, config_opt, call.inline_message_id),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("set_default_btn"),
                        "callback": self.inline__reset_default,
                        "args": (mod, config_opt),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ],
            ],
        )

    async def inline__configure(
        self,
        call: InlineCall,
        mod: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        btns = [
            {
                "text": param,
                "callback": self.inline__configure_option,
                "args": (mod, param),
                "kwargs": {"obj_type": obj_type},
            }
            for param in self.lookup(mod).config
        ]

        await call.edit(
            self.strings(
                "configuring_mod" if isinstance(obj_type, bool) else "configuring_lib"
            ).format(
                utils.escape_html(mod),
                "\n".join(
                    [
                        "âĢī¸ <code>{}</code>: <b>{}</b>".format(
                            utils.escape_html(key),
                            self._get_value(mod, key),
                        )
                        for key in self.lookup(mod).config
                    ]
                ),
            ),
            reply_markup=list(utils.chunks(btns, 2))
            + [
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__choose_category(self, call: typing.Union[Message, InlineCall]):
        await utils.answer(
            call,
            self.strings("choose_core"),
            reply_markup=[
                [
                    {
                        "text": self.strings("builtin"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": True},
                    },
                    {
                        "text": self.strings("external"),
                        "callback": self.inline__global_config,
                    },
                ],
                *(
                    [
                        [
                            {
                                "text": self.strings("libraries"),
                                "callback": self.inline__global_config,
                                "kwargs": {"obj_type": "library"},
                            }
                        ]
                    ]
                    if self.allmodules.libraries
                    and any(hasattr(lib, "config") for lib in self.allmodules.libraries)
                    else []
                ),
                [{"text": self.strings("close_btn"), "action": "close"}],
            ],
        )

    async def inline__global_config(
        self,
        call: InlineCall,
        page: int = 0,
        obj_type: typing.Union[bool, str] = False,
    ):
        if isinstance(obj_type, bool):
            to_config = [
                mod.strings("name")
                for mod in self.allmodules.modules
                if hasattr(mod, "config")
                and callable(mod.strings)
                and (mod.__origin__.startswith("<core") or not obj_type)
                and (not mod.__origin__.startswith("<core") or obj_type)
            ]
        else:
            to_config = [
                lib.name for lib in self.allmodules.libraries if hasattr(lib, "config")
            ]

        to_config.sort()

        kb = []
        for mod_row in utils.chunks(
            to_config[
                page
                * self._num_rows
                * self._row_size : (page + 1)
                * self._num_rows
                * self._row_size
            ],
            3,
        ):
            row = [
                {
                    "text": btn,
                    "callback": self.inline__configure,
                    "args": (btn,),
                    "kwargs": {"obj_type": obj_type},
                }
                for btn in mod_row
            ]
            kb += [row]

        if len(to_config) > self._num_rows * self._row_size:
            kb += self.inline.build_pagination(
                callback=functools.partial(
                    self.inline__global_config, obj_type=obj_type
                ),
                total_pages=ceil(len(to_config) / (self._num_rows * self._row_size)),
                current_page=page + 1,
            )

        kb += [
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__choose_category,
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ]
        ]

        await call.edit(
            self.strings(
                "configure" if isinstance(obj_type, bool) else "configure_lib"
            ),
            reply_markup=kb,
        )

    @loader.command(
        ru_doc="ĐĐ°ŅŅŅĐžĐ¸ŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        it_doc="Configura i moduli",
        de_doc="Konfiguriere Module",
        tr_doc="ModÃŧlleri yapÄąlandÄąr",
        uz_doc="Modullarni sozlash",
        es_doc="Configurar mÃŗdulos",
        kk_doc="ĐĐžĐ´ŅĐģŅĐ´ĐĩŅĐ´Ņ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅĐģĐ°Ņ",
        alias="cfg",
    )
    async def configcmd(self, message: Message):
        """Configure modules"""
        args = utils.get_args_raw(message)
        if self.lookup(args) and hasattr(self.lookup(args), "config"):
            form = await self.inline.form("đ", message, silent=True)
            mod = self.lookup(args)
            if isinstance(mod, loader.Library):
                type_ = "library"
            else:
                type_ = mod.__origin__.startswith("<core")

            await self.inline__configure(form, args, obj_type=type_)
            return

        await self.inline__choose_category(message)

    @loader.command(
        ru_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> <ĐŊĐ°ŅŅŅĐžĐšĐēĐ°> <ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ> - ŅŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐēĐžĐŊŅĐ¸ĐŗĐ° Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ"
        ),
        it_doc=(
            "<modulo> <impostazione> <valore> - imposta il valore della configurazione"
            " per il modulo"
        ),
        de_doc=(
            "<Modul> <Einstellung> <Wert> - Setze den Wert der Konfiguration fÃŧr das"
            " Modul"
        ),
        tr_doc="<modÃŧl> <ayar> <deÄer> - ModÃŧl iÃ§in yapÄąlandÄąrma deÄerini ayarla",
        uz_doc="<modul> <sozlash> <qiymat> - modul uchun sozlash qiymatini o'rnatish",
        es_doc=(
            "<mÃŗdulo> <configuraciÃŗn> <valor> - Establecer el valor de configuraciÃŗn"
        ),
        kk_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> <ĐŊĐ°ŅŅŅĐžĐšĐēĐ°> <ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ> - ĐŧĐžĐ´ŅĐģŅ Ō¯ŅŅĐŊ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸Ņ ĐŧĶĐŊŅĐŊ ĐžŅĐŊĐ°ŅŅ"
        ),
        alias="setcfg",
    )
    async def fconfig(self, message: Message):
        """<module_name> <property_name> <config_value> - set the config value for the module
        """
        args = utils.get_args_raw(message).split(maxsplit=2)

        if len(args) < 3:
            await utils.answer(message, self.strings("args"))
            return

        mod, option, value = args

        instance = self.lookup(mod)
        if not instance:
            await utils.answer(message, self.strings("no_mod"))
            return

        if option not in instance.config:
            await utils.answer(message, self.strings("no_option"))
            return

        instance.config[option] = value
        await utils.answer(
            message,
            self.strings(
                "option_saved"
                if isinstance(instance, loader.Module)
                else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
        )
