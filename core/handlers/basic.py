import logging
from datetime import datetime

from aiogram import Bot
from aiogram.types import Message
from aiogram.enums import ParseMode

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from config import messages
from core.utils import is_user_subscribed
from core.keyboards.inline_keybords import add_bot_to_chat_inl_keyboard, go_to_bot_ikb
from core.keyboards.reply_keybords import user_keyboard, admin_keyboard
from database.models.user import User


logger = logging.getLogger(__name__)


async def command_start(message: Message, bot: Bot, session: AsyncSession):
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    if chat_type == 'private':
        await message.delete()
        await message.answer(text=f'{messages.MESSAGE_ON_START_COMMAND}{message.from_user.full_name}',
                            reply_markup=user_keyboard(user_id))
        await is_user_subscribed(message, bot, session)
        
        
    elif chat_type != 'private':
        chat_admins = await bot.get_chat_administrators(chat_id=message.chat.id)
        chat_admins = [user_a.user.id for user_a in chat_admins]
        
        if user_id in chat_admins:
            try:
                await message.delete()
            except Exception as e:
                logger.error(e)
                
            await message.answer_photo(photo='AgACAgIAAxkBAAPmZcOjmZ-oSadgRaJXeQ02ATAwqZYAAgLaMRtJLxlKEdTyeWa_VDABAAMCAAN4AAM0BA',
                                        caption=messages.MESSAGE_ON_START_IN_GROUP,
                                        reply_markup=go_to_bot_ikb())


async def command_user_kb(message: Message):
    user_id = message.from_user.id
    await message.delete()
    
    await message.answer(text=messages.MESSAGE_ON_BACK_TO_USER_KB, reply_markup=user_keyboard(user_id))


async def command_create_theme(message: Message, bot: Bot):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_CREATE_THEME)
    # await bot.send_message(chat_id=-1001915761842, text='Text from BOT')


async def command_add_to_chat(message: Message):
    await message.delete()
    await message.answer_photo(
        photo='AgACAgIAAxkBAAPmZcOjmZ-oSadgRaJXeQ02ATAwqZYAAgLaMRtJLxlKEdTyeWa_VDABAAMCAAN4AAM0BA',
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