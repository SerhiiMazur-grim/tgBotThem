import logging
from datetime import datetime

from aiogram.types import Message
from aiogram.enums import ParseMode

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from config import messages
from config.api_keys import ADMINS
from core.keyboards.inline_keybords import add_bot_to_chat_inl_keyboard, go_to_bot_ikb
from core.keyboards.reply_keybords import user_keyboard, admin_keyboard
from database.models.user import User


logger = logging.getLogger(__name__)


async def command_start(message: Message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    if chat_type == 'private':
        await message.delete()
        await message.answer(text=messages.MESSAGE_ON_START_COMMAND, reply_markup=user_keyboard(user_id))
        
    elif chat_type != 'private' and str(user_id) in ADMINS:
        try:
            await message.delete()
        except Exception as e:
            logger.error(e)
            
        await message.answer_photo(photo='AgACAgIAAxkBAAIK1mV8QsjPPraAQ84AAeXm60eD5VhfnQAC1NIxG4mb4EtoJSNVJfQRiAEAAwIAA3gAAzME',
                                    caption=messages.MESSAGE_ON_START_IN_GROUP,
                                    reply_markup=go_to_bot_ikb())


async def command_user_kb(message: Message):
    user_id = message.from_user.id
    await message.delete()
    
    await message.answer(text=messages.MESSAGE_ON_BACK_TO_USER_KB, reply_markup=user_keyboard(user_id))


async def command_create_theme(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_CREATE_THEME)


async def command_add_to_chat(message: Message):
    await message.delete()
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIK1mV8QsjPPraAQ84AAeXm60eD5VhfnQAC1NIxG4mb4EtoJSNVJfQRiAEAAwIAA3gAAzME',
        caption=messages.MESSAGE_ON_ADD_TO_CHAT,
        reply_markup=add_bot_to_chat_inl_keyboard()
    )
        

async def command_faq(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_FAQ, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


async def command_admin_kb(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_ADMIN, reply_markup=admin_keyboard())


async def command_user_kb(message: Message):
    user_id = message.from_user.id
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_BACK_TO_USER_KB, reply_markup=user_keyboard(user_id))


async def bot_is_blocked(error, session: AsyncSession, user_id):
    try:
        if error.message == 'Forbidden: bot was blocked by the user':
            await session.execute(update(User).where(User.id==user_id).values(
                block_date=datetime.utcnow(),
                active=False
            ))
            await session.commit()
            
            logger.info(f'User {user_id} blocked the bot !')
        else:
            logger.error(error.message)
    except:
        logger.error(error)