# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html
# Netfoll Team modifided Hikka files for Netfoll
# đ https://github.com/MXRRI/Netfoll

import asyncio
import logging

from .. import loader, utils
from ..inline.types import BotInlineMessage, InlineCall

logger = logging.getLogger(__name__)


PRESETS = {
    "fun": [
        "https://mods.hikariatama.ru/aniquotes.py",
        "https://mods.hikariatama.ru/artai.py",
        "https://mods.hikariatama.ru/inline_ghoul.py",
        "https://mods.hikariatama.ru/lovemagic.py",
        "https://mods.hikariatama.ru/mindgame.py",
        "https://mods.hikariatama.ru/moonlove.py",
        "https://mods.hikariatama.ru/neko.py",
        "https://mods.hikariatama.ru/purr.py",
        "https://mods.hikariatama.ru/rpmod.py",
        "https://mods.hikariatama.ru/scrolller.py",
        "https://mods.hikariatama.ru/tictactoe.py",
        "https://mods.hikariatama.ru/trashguy.py",
        "https://mods.hikariatama.ru/truth_or_dare.py",
        "https://mods.hikariatama.ru/sticks.py",
        "https://mods.hikariatama.ru/premium_sticks.py",
        "https://heta.hikariatama.ru/MoriSummerz/ftg-mods/magictext.py",
        "https://heta.hikariatama.ru/HitaloSama/FTG-modules-repo/quotes.py",
        "https://heta.hikariatama.ru/HitaloSama/FTG-modules-repo/spam.py",
        "https://heta.hikariatama.ru/SkillsAngels/Modules/IrisLab.py",
        "https://heta.hikariatama.ru/Fl1yd/FTG-Modules/arts.py",
        "https://heta.hikariatama.ru/SkillsAngels/Modules/Complements.py",
        "https://heta.hikariatama.ru/Den4ikSuperOstryyPer4ik/Astro-modules/Compliments.py",
        "https://heta.hikariatama.ru/vsecoder/hikka_modules/mazemod.py",
    ],
    "chat": [
        "https://mods.hikariatama.ru/activists.py",
        "https://mods.hikariatama.ru/banstickers.py",
        "https://mods.hikariatama.ru/hikarichat.py",
        "https://mods.hikariatama.ru/inactive.py",
        "https://mods.hikariatama.ru/keyword.py",
        "https://mods.hikariatama.ru/tagall.py",
        "https://mods.hikariatama.ru/voicechat.py",
        "https://mods.hikariatama.ru/vtt.py",
        "https://heta.hikariatama.ru/SekaiYoneya/Friendly-telegram/BanMedia.py",
        "https://heta.hikariatama.ru/iamnalinor/FTG-modules/swmute.py",
        "https://heta.hikariatama.ru/GeekTG/FTG-Modules/filter.py",
    ],
    "service": [
        "https://mods.hikariatama.ru/account_switcher.py",
        "https://mods.hikariatama.ru/surl.py",
        "https://mods.hikariatama.ru/httpsc.py",
        "https://mods.hikariatama.ru/img2pdf.py",
        "https://mods.hikariatama.ru/latex.py",
        "https://mods.hikariatama.ru/pollplot.py",
        "https://mods.hikariatama.ru/sticks.py",
        "https://mods.hikariatama.ru/temp_chat.py",
        "https://mods.hikariatama.ru/vtt.py",
        "https://heta.hikariatama.ru/vsecoder/hikka_modules/accounttime.py",
        "https://heta.hikariatama.ru/vsecoder/hikka_modules/searx.py",
        "https://heta.hikariatama.ru/iamnalinor/FTG-modules/swmute.py",
    ],
    "downloaders": [
        "https://mods.hikariatama.ru/musicdl.py",
        "https://mods.hikariatama.ru/uploader.py",
        "https://mods.hikariatama.ru/porn.py",
        "https://mods.hikariatama.ru/web2file.py",
        "https://heta.hikariatama.ru/AmoreForever/amoremods/instsave.py",
        "https://heta.hikariatama.ru/CakesTwix/Hikka-Modules/tikcock.py",
        "https://heta.hikariatama.ru/CakesTwix/Hikka-Modules/InlineYouTube.py",
        "https://heta.hikariatama.ru/CakesTwix/Hikka-Modules/InlineSpotifyDownloader.py",
        "https://heta.hikariatama.ru/GeekTG/FTG-Modules/downloader.py",
        "https://heta.hikariatama.ru/Den4ikSuperOstryyPer4ik/Astro-modules/dl_yt_previews.py",
    ],
}


@loader.tds
class Presets(loader.Module):
    """Suggests new Netfoll users a packs of modules to load"""

    strings = {
        "name": "Presets",
        "_fun_title": "đĒŠ Entertainment modules",
        "_fun_desc": "Fun modules â animations, spam, entertainment, etc.",
        "_chat_title": "đĨ Group Administration Helpers",
        "_chat_desc": (
            "The collection of tools which will help to moderate your group chat â"
            " filters, notes, voice recognition, etc."
        ),
        "_service_title": "âī¸ Useful modules",
        "_service_desc": (
            "Really useful modules â account management, link shortener, search engine,"
            " etc."
        ),
        "_downloaders_title": "đĨ Downloaders",
        "_downloaders_desc": (
            "The collection of tools which will help you download/upload files from/to"
            " different sources â YouTube, TikTok, Instagram, Spotify, VK Music, etc."
        ),
        "welcome": (
            "đ <b>Hi there! Tired of scrolling through endless modules in channels? Let"
            " me suggest you some pre-made collections. If you need to call this menu"
            " again, simply send /presets to this bot!</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Modules in this collection:</b>\n\n{}"
        ),
        "back": "đ Back",
        "install": "đĻ Install",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installing preset"
            "</b> <code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installing preset"
            "</b> <code>{}</code> <b>({}/{} modules)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Installing module"
            " {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Preset"
            "</b> <code>{}</code> <b>installed!</b>"
        ),
        "already_installed": "â [Installed]",
    }

    strings_ru = {
        "_fun_title": "đĒŠ Đ Đ°ĐˇĐ˛ĐģĐĩĐēĐ°ŅĐĩĐģŅĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸",
        "_fun_desc": "ĐĐ°ĐąĐ°Đ˛ĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸ â Đ°ĐŊĐ¸ĐŧĐ°ŅĐ¸Đ¸, ŅĐŋĐ°Đŧ, Đ¸ĐŗŅŅ, Đ¸ Đ´Ņ.",
        "_chat_title": "đĨ ĐĐžĐ´ŅĐģĐ¸ Đ°Đ´ĐŧĐ¸ĐŊĐ¸ŅŅŅĐ¸ŅĐžĐ˛Đ°ĐŊĐ¸Ņ ŅĐ°ŅĐ°",
        "_chat_desc": (
            "ĐĐžĐģĐģĐĩĐēŅĐ¸Ņ ĐŧĐžĐ´ŅĐģĐĩĐš, ĐēĐžŅĐžŅŅĐĩ ĐŋĐžĐŧĐžĐŗŅŅ Đ˛Đ°Đŧ Đ°Đ´ĐŧĐ¸ĐŊĐ¸ŅŅŅĐ¸ŅĐžĐ˛Đ°ŅŅ ŅĐ°Ņ â ŅĐ¸ĐģŅŅŅŅ,"
            " ĐˇĐ°ĐŧĐĩŅĐēĐ¸, ŅĐ°ŅĐŋĐžĐˇĐŊĐ°Đ˛Đ°ĐŊĐ¸Đĩ ŅĐĩŅĐ¸, Đ¸ Đ´Ņ."
        ),
        "_service_title": "âī¸ ĐĐžĐģĐĩĐˇĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸",
        "_service_desc": (
            "ĐĐĩĐšŅŅĐ˛Đ¸ŅĐĩĐģŅĐŊĐž ĐŋĐžĐģĐĩĐˇĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸ â ŅĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ Đ°ĐēĐēĐ°ŅĐŊŅĐžĐŧ, ŅĐžĐēŅĐ°ŅĐ¸ŅĐĩĐģŅ ŅŅŅĐģĐžĐē,"
            " ĐŋĐžĐ¸ŅĐēĐžĐ˛Đ¸Đē, Đ¸ Đ´Ņ."
        ),
        "_downloaders_title": "đĨ ĐĐ°ĐŗŅŅĐˇŅĐ¸ĐēĐ¸",
        "_downloaders_desc": (
            "ĐĐžĐģĐģĐĩĐēŅĐ¸Ņ ĐŧĐžĐ´ŅĐģĐĩĐš, ĐēĐžŅĐžŅŅĐĩ ĐŋĐžĐŧĐžĐŗŅŅ Đ˛Đ°Đŧ ĐˇĐ°ĐŗŅŅĐļĐ°ŅŅ ŅĐ°ĐšĐģŅ Đ˛/Đ¸Đˇ ŅĐ°ĐˇĐģĐ¸ŅĐŊŅŅ(-Đĩ)"
            " Đ¸ŅŅĐžŅĐŊĐ¸ĐēĐžĐ˛(-Đ¸) â YouTube, TikTok, Instagram, Spotify, VK ĐŅĐˇŅĐēĐ°, Đ¸ Đ´Ņ."
        ),
        "welcome": (
            "đ <b>ĐŅĐ¸Đ˛ĐĩŅ! ĐŖŅŅĐ°Đģ ĐģĐ¸ŅŅĐ°ŅŅ ĐąĐĩŅŅĐ¸ŅĐģĐĩĐŊĐŊĐžĐĩ ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Đž ĐŧĐžĐ´ŅĐģĐĩĐš Đ˛ ĐēĐ°ĐŊĐ°ĐģĐ°Ņ? ĐĐžĐŗŅ"
            " ĐŋŅĐĩĐ´ĐģĐžĐļĐ¸ŅŅ ŅĐĩĐąĐĩ ĐŊĐĩŅĐēĐžĐģŅĐēĐž ĐŗĐžŅĐžĐ˛ŅŅ ĐŊĐ°ĐąĐžŅĐžĐ˛. ĐŅĐģĐ¸ ŅĐĩĐąĐĩ ĐŋĐžĐŊĐ°Đ´ĐžĐąĐ¸ŅŅŅ ĐŋĐžĐ˛ŅĐžŅĐŊĐž"
            " Đ˛ŅĐˇĐ˛Đ°ŅŅ ŅŅĐž ĐŧĐĩĐŊŅ, ĐžŅĐŋŅĐ°Đ˛Ņ ĐŧĐŊĐĩ ĐēĐžĐŧĐ°ĐŊĐ´Ņ /presets</b>"
        ),
        "preset": "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>ĐĐžĐ´ŅĐģĐ¸ Đ˛ ŅŅĐžĐŧ ĐŊĐ°ĐąĐžŅĐĩ:</b>\n\n{}",
        "back": "đ ĐĐ°ĐˇĐ°Đ´",
        "install": "đĻ ĐŖŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ° ĐŊĐ°ĐąĐžŅĐ°"
            " >/b><code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ° ĐŊĐ°ĐąĐžŅĐ°"
            "</b> <code>{}</code> <b>({}/{} ĐŧĐžĐ´ŅĐģĐĩĐš)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ° ĐŧĐžĐ´ŅĐģŅ {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ĐĐ°ĐąĐžŅ"
            "</b> <code>{}</code> <b>ŅŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ!</b>"
        ),
        "already_installed": "â [ĐŖŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ]",
    }

    async def client_ready(self):
        self._markup = utils.chunks(
            [
                {
                    "text": self.strings(f"_{preset}_title"),
                    "callback": self._preset,
                    "args": (preset,),
                }
                for preset in PRESETS
            ],
            1,
        )

        if self.get("sent"):
            return

        self.set("sent", True)
        await self._menu()

    async def _menu(self):
        await self.inline.bot.send_message(
            self._client.tg_id,
            self.strings("welcome"),
            reply_markup=self.inline.generate_markup(self._markup),
        )

    async def _back(self, call: InlineCall):
        await call.edit(self.strings("welcome"), reply_markup=self._markup)

    async def _install(self, call: InlineCall, preset: str):
        await call.delete()
        m = await self._client.send_message(
            self.inline.bot_id,
            self.strings("installing").format(preset),
        )
        for i, module in enumerate(PRESETS[preset]):
            await m.edit(
                self.strings("installing_module").format(
                    preset, i, len(PRESETS[preset]), module
                )
            )
            try:
                await self.lookup("loader").download_and_install(module, None)
            except Exception:
                logger.exception("Failed to install module %s", module)

            await asyncio.sleep(1)

        if self.lookup("loader").fully_loaded:
            self.lookup("loader").update_modules_in_db()

        await m.edit(self.strings("installed").format(preset))
        await self._menu()

    def _is_installed(self, link: str) -> bool:
        return any(
            link.strip().lower() == installed.strip().lower()
            for installed in self.lookup("loader").get("loaded_modules", {}).values()
        )

    async def _preset(self, call: InlineCall, preset: str):
        await call.edit(
            self.strings("preset").format(
                self.strings(f"_{preset}_title"),
                self.strings(f"_{preset}_desc"),
                "\n".join(
                    map(
                        lambda x: x[0],
                        sorted(
                            [
                                (
                                    "{} <b>{}</b>".format(
                                        (
                                            self.strings("already_installed")
                                            if self._is_installed(link)
                                            else "âĢī¸"
                                        ),
                                        link.rsplit("/", maxsplit=1)[1].split(".")[0],
                                    ),
                                    int(self._is_installed(link)),
                                )
                                for link in PRESETS[preset]
                            ],
                            key=lambda x: x[1],
                            reverse=True,
                        ),
                    )
                ),
            ),
            reply_markup=[
                {"text": self.strings("back"), "callback": self._back},
                {
                    "text": self.strings("install"),
                    "callback": self._install,
                    "args": (preset,),
                },
            ],
        )

    async def aiogram_watcher(self, message: BotInlineMessage):
        if message.text != "/presets" or message.from_user.id != self._client.tg_id:
            return

        await self._menu()
