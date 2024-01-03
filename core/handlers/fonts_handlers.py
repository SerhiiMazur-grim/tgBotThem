from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from config import messages
from core.keyboards.inline_keybords import fonts_ikb
from core.utils import ch_text_font


USER_TEXT = {}


async def font_catalog(message: Message, bot: Bot):
    user_id = message.from_user.id
    USER_TEXT[user_id] = ''
    await message.delete()
    await message.answer(text=messages.MESSAGE_SEND_ME_TEXT)


async def get_text_from_user(message: Message, bot: Bot):
    user_id = message.from_user.id
    text = message.text[2:]
    USER_TEXT[user_id] = text
    await message.reply(text=messages.MESSAGE_CHOICE_FONT, reply_markup=fonts_ikb())


async def change_font_in_text(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    font = callback_query.data
    text = USER_TEXT[user_id]
    new_text = await ch_text_font(text, font)
    await callback_query.message.answer(text=new_text)
