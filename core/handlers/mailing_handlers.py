from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.types.input_media_animation import InputMediaAnimation
from aiogram.types.input_media_document import InputMediaDocument
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types.input_media_video import InputMediaVideo

from config import messages
from core.utils import is_admin
from core.keyboards.inline_keybords import send_post_ikb, abort_create_post_ikb
from core.database import get_chats_id_from_db, get_private_chats_id_from_db, get_group_chats_id_from_db


SEND_DATA = {}


async def create_mailing(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.delete()
        SEND_DATA[user_id] = {}
        SEND_DATA[user_id]['self_group'] = []
        SEND_DATA[user_id]['text'] = ''
        SEND_DATA[user_id]['forward'] = None
        SEND_DATA[user_id]['forward_group'] = []
        SEND_DATA[user_id]['key'] = ''
        
        await message.answer(text=messages.MESSAGE_GIVE_ME_POST, parse_mode=ParseMode.HTML, reply_markup=abort_create_post_ikb())


async def forward_post_message(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_admin(user_id) and SEND_DATA.get(user_id) != None:
        SEND_DATA[user_id]['forward'] = message
        SEND_DATA[user_id]['key'] = 'forward'
    


async def save_media_group_post_media(message: Message):
    user_id = message.from_user.id
    if is_admin(user_id) and SEND_DATA.get(user_id) != None:
        if message.forward_from or message.forward_from_chat:
            key = 'forward_group'
        else: key = 'self_group'
        
        if message.text:
            text = message.text[5:]
            SEND_DATA[user_id]['text'] = text
            SEND_DATA[user_id]['key'] = 'text'
            return
        
        elif message.animation:
            media = message.animation.file_id
            caption = message.caption
            caption_entities = message.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]
            animation = InputMediaAnimation(media=media, caption=caption, caption_entities=caption_entities)
            SEND_DATA[user_id][key].append(animation)
            SEND_DATA[user_id]['key'] = key
            return

        elif message.document:
            media = message.document.file_id
            caption = message.caption
            caption_entities = message.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]
            document = InputMediaDocument(media=media, caption=caption, caption_entities=caption_entities)
            SEND_DATA[user_id][key].append(document)
            SEND_DATA[user_id]['key'] = key
            return

        elif message.audio:
            media = message.audio.file_id
            caption = message.caption
            caption_entities = message.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]
            audio = InputMediaAudio(media=media, caption=caption, caption_entities=caption_entities)
            SEND_DATA[user_id][key].append(audio)
            SEND_DATA[user_id]['key'] = key
            return

        elif message.photo:
            media = message.photo[-1].file_id
            caption = message.caption
            caption_entities = message.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]
            photo = InputMediaPhoto(media=media, caption=caption, caption_entities=caption_entities)
            SEND_DATA[user_id][key].append(photo)
            SEND_DATA[user_id]['key'] = key
            return

        elif message.video:
            media = message.video.file_id
            caption = message.caption
            caption_entities = message.caption_entities
            if caption.startswith('POST\n'):
                caption = caption[5:]
            video = InputMediaVideo(media=media, caption=caption, caption_entities=caption_entities)
            SEND_DATA[user_id][key].append(video)
            SEND_DATA[user_id]['key'] = key
            return


async def view_post_media(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.delete()
        if SEND_DATA.get(user_id) != None:
            key = SEND_DATA[user_id]['key']
            if key == 'text':
                await message.answer(text=SEND_DATA[user_id]['text'], reply_markup=send_post_ikb())
            elif key == 'forward':
                await SEND_DATA[user_id]['forward'].send_copy(chat_id=message.chat.id)
                await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())
            else:
                await message.answer_media_group(media=SEND_DATA[user_id][key])
                await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())
        else:
            await message.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_all(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        chats = await get_chats_id_from_db()
        if SEND_DATA.get(user_id) != None:
            key = SEND_DATA[user_id]['key']
            for chat in chats:
                if key == 'text':
                    await bot.send_message(chat_id=chat, text=SEND_DATA[user_id][key])
                elif key == 'forward':
                    await SEND_DATA[user_id]['forward'].send_copy(chat_id=chat)
                else:
                    await bot.send_media_group(chat_id=chat, media=SEND_DATA[user_id][key])
            SEND_DATA.pop(user_id)
            await callback_query.message.delete()
                
        else:
            await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_private(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        chats = await get_private_chats_id_from_db()
        if SEND_DATA.get(user_id) != None:
            key = SEND_DATA[user_id]['key']
            for chat in chats:
                if key == 'text':
                    await bot.send_message(chat_id=chat, text=SEND_DATA[user_id][key])
                elif key == 'forward':
                    await SEND_DATA[user_id]['forward'].send_copy(chat_id=chat)
                else:
                    await bot.send_media_group(chat_id=chat, media=SEND_DATA[user_id][key])
            SEND_DATA.pop(user_id)
            await callback_query.message.delete()
                
        else:
            await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_group(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        chats = await get_group_chats_id_from_db()
        if SEND_DATA.get(user_id) != None:
            key = SEND_DATA[user_id]['key']
            for chat in chats:
                if key == 'text':
                    await bot.send_message(chat_id=chat, text=SEND_DATA[user_id][key])
                elif key == 'forward':
                    await SEND_DATA[user_id]['forward'].send_copy(chat_id=chat)
                else:
                    await bot.send_media_group(chat_id=chat, media=SEND_DATA[user_id][key])
            SEND_DATA.pop(user_id)
            await callback_query.message.delete()
                
        else:
            await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def delete_post(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        SEND_DATA.pop(user_id)
        await callback_query.message.delete()
        await callback_query.answer(text=messages.MESSAGE_DELETE_POST)


async def abort_create_post(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        SEND_DATA.pop(user_id)
        await callback_query.message.delete()
