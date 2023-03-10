# ---------------------------------------------------------------------------------
#  /\_/\  ๐ This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  ๐ Licensed under the GNU AGPLv3.
#  > ^ <   โ ๏ธ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: inline_bot_manager
# Description: Control over your Inline bot!
# Author: Den4ikSuperOstryyPer4ik
# Commands:
# .inlinebothelp | .ibsetname | .ibsetqtext | .ibsetdescription | .ibsetabout
# .ibcheckname
# ---------------------------------------------------------------------------------


#               _             __  __           _       _
#     /\       | |           |  \/  |         | |     | |
#    /  \   ___| |_ _ __ ___ | \  / | ___   __| |_   _| | ___  ___
#   / /\ \ / __| __| '__/ _ \| |\/| |/ _ \ / _` | | | | |/ _ \/ __|
#  / ____ \\__ \ |_| | | (_) | |  | | (_) | (_| | |_| | |  __/\__ \
# /_/    \_\___/\__|_|  \___/|_|  |_|\___/ \__,_|\__,_|_|\___||___/
#
#               ยฉ Copyright 2022
#
#      https://t.me/Den4ikSuperOstryyPer4ik
#                      and
#             https://t.me/ToXicUse
#
#       ๐ Licensed under the GNU AGPLv3
#    https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @AstroModules
# meta pic: https://img.icons8.com/plasticine/200/000000/bot.png
# meta banner: ะตัะต ะฝะตัั :(
# scope: hikka_only
# scope: hikka_min 1.3.0

import logging

from .. import loader
from .. import utils as u

logger = logging.getLogger(__name__)


@loader.tds
class InlineBotManagerMod(loader.Module):
    """Control over your Inline bot!"""

    strings = {
        "name": "InlineBotManager",
        "no_args": (
            "No arguments :( | Read, how to use the module, command: <code>{}>/code>"
        ),
        "...-set": (
            "<b>{} for your inline bot(@{}) successfully set to <code>{}</code></b>"
        ),
        "error": "An error has occurred.",
        "namea": "Name",
        "inline-text": "Inline-Text",
        "about-text": "About",
        "description-text": "Description",
        "help-mod": """<b><i>โข<u>Instructions for the module:</u>
------------------------------------------------
โข<u>Information about the module:</u>
    โขModule name --> <code>InlineBotManager</code>
    โขModule description --> <code>Control over your Inline bot!</code>
    โขLink to the module(to download) --> <code></code>
    โขUnload the module --> <code>{prefix}unloadmod InlineBotManager</code>
    โขYour inline botname --> <code>{}</code>
    โขYour inline bot username --> @{}
------------------------------------------------
โข Commands:
    โข <code>{prefix}ibcheckname</code> --> check bot name to be: "<code>๐ Hikka Userbot of {your nickname}</code>"
    --------------------------------------------
    โข <code>{prefix}ibsetname </code><name> --> set a name for your Inline Bot
    Command example:
    <code>{prefix}ibsetname DSOP-UserBot</code>
    --------------------------------------------
    โข <code>{prefix}ibsetqtext </code><text> --> set text instead of "InlineQuery" for your Inline Bot
    Command example:
    <code>{prefix}ibsetqtext UserBot-Inline-Query</code>
    --------------------------------------------
    โข <code>{prefix}ibsetdescription </code><text> --> change the information Description the inline bot
    Command example:
    <code>{prefix}ibsetdescription DSOP-UserBot</code>
    --------------------------------------------
    โข <code>{prefix}ibsetabout </code><text> --> change the text about the information about the inline bot
    Command example:
    <code>{prefix}ibsetabout DSOP-UserBot-about</code>
------------------------------------------------</i></b>""",
        "check-yes": "<b>Bot name checked successfully!\nIt's correct.</b>",
        "check-no": (
            "<b>Your inline bot name(@{}) was successfully checked! Result: bot name"
            " didn't match account name, bot name was changed from <code>{}</code> to"
            " <code>{}</code></b>"
        ),
        "_cfg_check_name": (
            "Check and change the name of your inline bot after every restart?"
        ),
    }

    strings_ru = {
        "_cls_doc": """ะฃะฟัะฐะฒะปะตะฝะธะต ะฝะฐะด ัะฒะพะธะผ Inline ะฑะพัะพะผ!""",
        "no_args": (
            "ะะตั ะฐัะณัะผะตะฝัะพะฒ :( | ะัะพัะธัะฐะนัะต, ะบะฐะบ ะฟะพะปัะทะพะฒะฐัััั ะผะพะดัะปะตะผ, ะบะพะผะฐะฝะดะพะน:"
            " <code>{}</code>"
        ),
        "...-set": (
            "<b>{} ะดะปั ะฒะฐัะตะณะพ ะธะฝะปะฐะนะฝ-ะฑะพัะฐ(@{}) ััะฟะตัะฝะพ ัััะฐะฝะพะฒะปะตะฝ(-ะพ/-ะฐ) ะฝะฐ"
            " <code>{}</code></b>"
        ),
        "namea": "ะะผั",
        "inline-text": "Inline-ะขะตะบัั",
        "about-text": "ะขะตะบัั ะพะฑ ะธะฝัะพัะผะฐัะธะธ",
        "description-text": "ะะฝัะพัะผะฐัะธั",
        "error": "ะัะพะธะทะพัะปะฐ ะพัะธะฑะบะฐ.",
        "help-mod": """<b><i>โข<u>ะะฝััััะบัะธั ะบ ะผะพะดัะปั:</u>
------------------------------------------------
โข<u>ะะฝัะพัะผะฐัะธั ะพ ะผะพะดัะปะต:</u>
    โขะะฐะทะฒะฐะฝะธะต ะผะพะดัะปั --> <code>InlineBotManager</code>
    โขะะฟะธัะฐะฝะธะต ะผะพะดัะปั --> <code>ะฃะฟัะฐะฒะปะตะฝะธะต ะฝะฐะด ัะฒะพะธะผ Inline ะฑะพัะพะผ!</code>
    โขะกััะปะบะฐ ะฝะฐ ะผะพะดัะปั(ะดะปั ะทะฐะณััะทะบะธ) --> <code></code>
    โขะัะณััะทะธัั ะผะพะดัะปั --> <code>{prefix}unloadmod InlineBotManager</code>
------------------------------------------------
โขะะฝัะพัะผะฐัะธั ะพ ะฒะฐัะตะผ ะะฝะปะฐะนะฝ-ะะพัะต:
    ------
    โขะะผั ะฑะพัะฐ --> <code>{}</code>
    ----------------------
    โขะฎะทะตัะฝะตะนะผ ะฑะพัะฐ --> @{}
------------------------------------------------
โขะะพะผะฐะฝะดั:
    โข <code>{prefix}ibcheckname</code> --> ะฟัะพะฒะตัะธัั ะธะผั ะฑะพัะฐ, ััะพะฑั ะพะฝะพ ะฑัะปะพ: "๐ Hikka Userbot of (ะฒะฐั ะฝะธะบ-ะฝะตะนะผ)"
------------------------------------------------
    โข <code>{prefix}ibsetname </code><ะธะผั> --> ัััะฐะฝะพะฒะธัั ะธะผั ะดะปั ะฒะฐัะตะณะพ ะะฝะปะฐะนะฝ-ะะพัะฐ
    ะัะธะผะตั ะบะพะผะฐะฝะดั:
    <code>{prefix}ibsetname DSOP-UserBot</code>
------------------------------------------------
    โข <code>{prefix}ibsetqtext </code><ัะตะบัั> --> ัััะฐะฝะพะฒะธัั ัะตะบัั ะฒะผะตััะพ "InlineQuery" ะดะปั ะฒะฐัะตะณะพ ะะฝะปะฐะนะฝ-ะะพัะฐ
    ะัะธะผะตั ะบะพะผะฐะฝะดั:
    <code>{prefix}ibsetqtext UserBot-Inline-Query</code>
------------------------------------------------
    โข <code>{prefix}ibsetdescription </code><ัะตะบัั> --> ะธะทะผะตะฝะธัั ะธะฝัะพัะผะฐัะธั ะพ ะธะฝะปะฐะนะฝ-ะฑะพัะต
    ะัะธะผะตั ะบะพะผะฐะฝะดั:
    <code>{prefix}ibsetdescription DSOP-UserBot</code>
------------------------------------------------
    โข <code>{prefix}ibsetabout </code><ัะตะบัั> --> ะธะทะผะตะฝะธัั ัะตะบัั ะพะฑ ะธะฝัะพัะผะฐัะธะธ ะพ ะธะฝะปะฐะนะฝ-ะฑะพัะต
    ะัะธะผะตั ะบะพะผะฐะฝะดั:
    <code>{prefix}ibsetabout DSOP-UserBot-about</code>
------------------------------------------------</i></b>""",
        "ib-help": """<b>----------------------
</b>""",
        "check-yes": "<b>ะะผั ะฑะพัะฐ ััะฟะตัะฝะพ ะฟัะพะฒะตัะตะฝะพ!\nะะฝะพ ะฒะตัะฝะพะต.</b>",
        "check-no": (
            "<b>ะะผั ะฒะฐัะตะณะพ ะธะฝะปะฐะนะฝ-ะฑะพัะฐ(@{}) ะฑัะปะพ ััะฟะตัะฝะพ ะฟัะพะฒะตัะตะฝะพ! ะ ะตะทัะปััะฐั: ะธะผั ะฑะพัะฐ"
            " ะฝะต ัะพะพัะฒะตัััะฒะพะฒะฐะปะพ ะธะผะตะฝะธ ะฐะบะบะฐัะฝัะฐ, ะธะผั ะฑะพัะฐ ะฑัะปะพ ัะผะตะฝะตะฝะพ ั"
            " <code>{}</code> ะฝะฐ <code>{}</code></b>"
        ),
        "_cfg_check_name": (
            "ะัะพะฒะตัััั ะธ ะธะทะผะตะฝััั ะธะผั ะฒะฐัะตะณะพ ะธะฝะปะฐะนะฝ-ะฑะพัะฐ ะฟะพัะปะต ะบะฐะถะดะพะณะพ ัะตััะฐััะฐ?"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "check_name",
                False,
                lambda: self.strings("_cfg_check_name"),
                validator=loader.validators.Boolean(),
            )
        )

    @loader.command(ru_doc="--> ะัะพัะผะพััะตัั ะฟะพะผะพัั ะฟะพ ััะพะผั ะผะพะดัะปั")
    async def inlinebothelpcmd(self, message):
        """--> Check help for this module"""
        await message.delete()
        name = self.bot.first_name
        username = self.bot.username
        await self.client.send_message(
            message.peer_id,
            self.strings("help-mod").format(
                name,
                username,
                prefix=self.get_prefix(),
            ),
        )

    @loader.command(ru_doc="<ะธะผั> --> ะธะทะผะตะฝะธัั ะธะผั ะดะปั ะฒะฐัะตะณะพ ะะฝะปะฐะนะฝ-ะะพัะฐ")
    async def ibsetnamecmd(self, message):
        """<name> --> change Name for your Inline-Bot"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setname")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(args)
                await conv.mark_read()

            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("namea"), self.inline.bot_username, args
                ),
            )

    @loader.command(
        ru_doc="<ัะตะบัั> --> ะธะทะผะตะฝะธัั ัะตะบัั ะฒ InlineQuery ะดะปั ะฒะฐัะตะณะพ ะะฝะปะฐะนะฝ-ะะพัะฐ"
    )
    async def ibsetqtextcmd(self, message):
        """<text> --> change text in InlineQuery for your Inline-Bot"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setinline")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(args)
                await conv.mark_read()

            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("inline-text"), self.inline.bot_username, args
                ),
            )

    @loader.command(ru_doc="<ัะตะบัั> --> ะธะทะผะตะฝะธัั ะธะฝัะพัะผะฐัะธั ะพ ะธะฝะปะฐะนะฝ-ะฑะพัะต")
    async def ibsetdescriptioncmd(self, message):
        """<description> --> change inline-bot description"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setdescription")
                await conv.mark_read()
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.mark_read()
                await conv.send_message(args)
            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("description-text"), self.inline.bot_username, args
                ),
            )

    @loader.command(ru_doc="<ัะตะบัั> --> ะธะทะผะตะฝะธัั ัะตะบัั ะพะฑ ะธะฝัะพัะผะฐัะธะธ ะพ ะธะฝะปะฐะนะฝ-ะฑะพัะต")
    async def ibsetaboutcmd(self, message):
        """<about> --> change inline-bot about text"""
        args = u.get_args_raw(message)
        if not args:
            command = f"{self.get_prefix()}inlinebothelp"
            await u.answer(message, self.strings("no_args").format(command))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setabouttext")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(args)
                await conv.mark_read()

            await u.answer(
                message,
                self.strings("...-set").format(
                    self.strings("about-text"), self.inline.bot_username, args
                ),
            )

    @loader.command(
        ru_doc="""-->ะฟัะพะฒะตัะธัั ะธะผั ะฑะพัะฐ, ััะพะฑั ะพะฝะพ ะฑัะปะพ: "๐ Hikka Userbot of {ะฒะฐั ะฝะธะบ}" """
    )
    async def ibchecknamecmd(self, message):
        """-->check bot name to be: "๐ Hikka Userbot of {your nickname}" """
        bot_name = self.bot.first_name
        acc_name = self.acc.first_name
        norm_nameb = f"๐ Hikka Userbot of {acc_name}"
        if bot_name == norm_nameb:
            await u.answer(message, self.strings("check-yes"))
            logger.debug(self.strings("check-yes"))
        else:
            async with self.client.conversation(self.botfather) as conv:
                await conv.send_message("/setname")
                await conv.send_message(f"@{self.inline.bot_username}")
                await conv.send_message(norm_nameb)
                await conv.mark_read()

            logger.info(
                self.strings("check-no").format(self.bot.username, bot_name, norm_nameb)
            )
            await u.answer(
                message,
                self.strings("check-no").format(
                    self.inline.bot_username, bot_name, norm_nameb
                ),
            )

    async def client_ready(self, *_):
        self.botfather = "@BotFather"
        self.bot = await self.inline.bot.get_me()
        self.acc = await self.client.get_me()
        if self.config["check_name"]:
            m = await self.client.send_message("me", f"{self.get_prefix()}ibcheckname")
            await self.ibchecknamecmd(m)
