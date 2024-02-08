import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from config.api_keys import CHANNEL_IDS
from config.api_keys import ADMINS
from config.fonts import FONTS
from config import messages
from core.keyboards.inline_keybords import subscribe_keyboard
from database.models.user import User
# from core.database import start_db
# from core.commands import set_commands


# async def start_bot(bot: Bot):
    # await start_db()
    # await set_commands(bot)


async def is_user_subscribed(message, bot: Bot, session: AsyncSession):

    # Перевірка підписки користувача на кожен канал зі списку channel_ids
    checked_channels = []
    user_id = message.from_user.id
    if str(user_id) in ADMINS:
        return True
    
    for channel_id in CHANNEL_IDS:
        member = await Bot.get_chat_member(self=bot, chat_id=channel_id, user_id=user_id)

        # Перевірка, чи користувач є учасником каналу та має статус "member" або "creator"
        if member.status == 'member' or member.status == 'creator':
            continue
        else:
            checked_channels.append(channel_id)

    if not checked_channels:
        return True
    else:
        
        await session.execute(update(User).where(User.id==user_id).values(sub=False))
        await session.commit()
        
        if type(message) == Message:
            await message.answer(text=messages.MESSAGE_YOU_NOT_SUBSCRIBE,
                                 reply_markup=subscribe_keyboard(checked_channels))
        elif type(message) == CallbackQuery:
            await message.message.answer(text=messages.MESSAGE_YOU_NOT_SUBSCRIBE,
                                 reply_markup=subscribe_keyboard(checked_channels))
        return False


async def sub_checker(callback_query: CallbackQuery, bot: Bot, session: AsyncSession):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    
    if await is_user_subscribed(callback_query, bot, session):
        await callback_query.message.answer(text=messages.SUBSCRIBE_CHECKED)
        await session.execute(update(User).where(User.id==user_id).values(sub=True))
        await session.commit()


async def dell_data(user_data, chat_id):

    android = os.path.join('android', 'theme', str(chat_id))
    iphone = os.path.join('ios', 'theme', str(chat_id))
    desktop = os.path.join('desktop', 'theme', str(chat_id))
    download_img = os.path.join('download_photo', user_data[chat_id]["image_name"])
    gener_img = os.path.join('gener_image', user_data[chat_id]["colors_image"])

    for folder in [android, iphone, desktop]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

    try:
        if os.path.isfile(download_img):
            os.remove(download_img)
    except Exception as e:
        print(e)

    try:
        if os.path.isfile(gener_img):
            os.remove(gener_img)
    except Exception as e:
        print(e)


async def ch_text_font(text, font):
    if text:
        converted_text = ''.join(FONTS[font].get(c, c) for c in text)
        return converted_text


async def hex_to_rgba_v2(hex_colors):
    rgb_colors = []
    for hex_color in hex_colors:
        hex_color = hex_color.lstrip('#')

        if len(hex_color) == 6:
            rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
            rgb_colors.append(rgb)
        elif len(hex_color) == 8:
            rgba = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4, 6))
            rgb_colors.append(rgba)
    
    return rgb_colors
