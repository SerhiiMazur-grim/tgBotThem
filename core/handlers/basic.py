import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from config.messages import MESSAGE_ON_START_COMMAND, MESSAGE_YOU_NOT_SUBSCRIBE, SUBSCRIBE_CHECKED
from config.telegram_chats import CHANNEL_IDS
from core.commands import set_commands
from core.keyboards.inline_keybords import subscribe_keyboard


async def start_bot(bot: Bot):
    await set_commands(bot)


async def command_start(message: Message, bot: Bot):
    await message.delete()
    if await is_user_subscribed(message=message, bot=bot):
        await message.answer(text=MESSAGE_ON_START_COMMAND)


async def is_user_subscribed(message, bot: Bot):

    # Перевірка підписки користувача на кожен канал зі списку channel_ids
    checked_channels = []
    for channel_id in CHANNEL_IDS.keys():
        member = await Bot.get_chat_member(self=bot, chat_id=channel_id, user_id=message.from_user.id)

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
            await message.answer(text=MESSAGE_YOU_NOT_SUBSCRIBE,
                                 reply_markup=subscribe_keyboard(checked_channels))
        elif type(message) == CallbackQuery:
            await message.message.answer(text=MESSAGE_YOU_NOT_SUBSCRIBE,
                                 reply_markup=subscribe_keyboard(checked_channels))
        return False


async def sub_checker(callback_query: CallbackQuery, bot: Bot):
    if await is_user_subscribed(callback_query, bot):
        await callback_query.message.answer(text=SUBSCRIBE_CHECKED)
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
