import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from config.telegram_chats import CHANNEL_IDS
from config.api_keys import ADMINS
from config.fonts import FONTS
from config import messages
from core.keyboards.inline_keybords import subscribe_keyboard
from core.database import start_db
from core.commands import set_commands


async def start_bot(bot: Bot):
    # await set_commands(bot)
    await start_db()


def is_admin(user_id):
    return str(user_id) in ADMINS


def is_private_chat(message):
    if message.chat.type == 'private':
        return True
    return False


async def is_user_subscribed(message, bot: Bot):

    # Перевірка підписки користувача на кожен канал зі списку channel_ids
    checked_channels = []
    user_id = message.from_user.id
    if is_admin(user_id):
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
        # Якщо користувач не підписаний ні на один з каналів, створимо і покажемо інлайнову клавіатуру
        if type(message) == Message:
            await message.answer(text=messages.MESSAGE_YOU_NOT_SUBSCRIBE,
                                 reply_markup=subscribe_keyboard(checked_channels))
        elif type(message) == CallbackQuery:
            await message.message.answer(text=messages.MESSAGE_YOU_NOT_SUBSCRIBE,
                                 reply_markup=subscribe_keyboard(checked_channels))
        return False


async def sub_checker(callback_query: CallbackQuery, bot: Bot):
    if await is_user_subscribed(callback_query, bot):
        await callback_query.message.answer(text=messages.SUBSCRIBE_CHECKED)
        await callback_query.answer()


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
    converted_text = ''.join(FONTS[font].get(c, c) for c in text)
    return converted_text
