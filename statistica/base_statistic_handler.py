from aiogram.types import Message

from config import messages
from core import inline_keybords, reply_keybords


async def statistic_menu(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_IS_STATISTIC_MENU,
                         reply_markup=reply_keybords.admin_statistic_menu_kb())


async def active_statistic_menu(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_PERIOD_OF_ACTIVE_CHOICE,
                         reply_markup=inline_keybords.active_statistic_menu_ikb())
