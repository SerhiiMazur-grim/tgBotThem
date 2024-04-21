import os
import subprocess
import logging

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.methods import TelegramMethod
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from core.keyboards.inline_keybords import abort_set_wallpaper_ikb
from config import messages
from core.states import SetWallpaperState


logger = logging.getLogger(__name__)


async def restart_bot(message: Message):
    await message.delete()
    
    command = "sudo systemctl restart theme_bot"
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        logger.exception(e)
        await message.answer('Что-то пошло не так, смотри логи')
