from aiogram import Bot
from aiogram.types import Message

from config import messages
from core.keyboards.inline_keybords import add_bot_to_chat_inl_keyboard
from core.keyboards.reply_keybords import user_keyboard, admin_keyboard
from core.utils import is_user_subscribed, is_private_chat, is_admin
from core.database import add_user_to_db


async def command_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_type = message.chat.type
    
    await add_user_to_db(user_id, chat_id, chat_type)
    
    if is_private_chat(message):
        await message.delete()
        if await is_user_subscribed(message=message, bot=bot):
            await message.answer(text=messages.MESSAGE_ON_START_COMMAND, reply_markup=user_keyboard(user_id))
    else:
        await message.answer_photo(photo='AgACAgIAAxkBAAIK1mV8QsjPPraAQ84AAeXm60eD5VhfnQAC1NIxG4mb4EtoJSNVJfQRiAEAAwIAA3gAAzME',
                                    caption=messages.MESSAGE_ON_START_IN_GROUP,
                                    reply_markup=None)


async def command_create_theme(message: Message, bot: Bot):
    if is_private_chat(message):
        await message.delete()
        if await is_user_subscribed(message=message, bot=bot):
            await message.answer(text=messages.MESSAGE_ON_CREATE_THEME)


async def command_add_to_chat(message: Message, bot: Bot):
    if is_private_chat(message):
        await message.delete()
        if await is_user_subscribed(message=message, bot=bot):
            await message.answer_photo(
                photo='AgACAgIAAxkBAAIK1mV8QsjPPraAQ84AAeXm60eD5VhfnQAC1NIxG4mb4EtoJSNVJfQRiAEAAwIAA3gAAzME',
                caption=messages.MESSAGE_ON_ADD_TO_CHAT,
                reply_markup=add_bot_to_chat_inl_keyboard()
            )
        

async def command_faq(message: Message, bot: Bot):
    if is_private_chat(message):
        await message.delete()
        if await is_user_subscribed(message=message, bot=bot):
            await message.answer(text=messages.MESSAGE_ON_FAQ, disable_web_page_preview=True)


async def command_admin_kb(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_private_chat(message) and is_admin(user_id):
        await message.delete()
        await message.answer(text=messages.MESSAGE_ON_ADMIN, reply_markup=admin_keyboard())


async def command_user_kb(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_private_chat(message) and is_admin(user_id):
        await message.delete()
        await message.answer(text=messages.MESSAGE_ON_BACK_TO_USER_KB, reply_markup=user_keyboard(user_id))
