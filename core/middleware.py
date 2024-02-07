from datetime import datetime, timedelta, time
import os
import logging
from typing import Callable, Awaitable, Dict, Any
import json

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from aiogram.types.input_media_animation import InputMediaAnimation
from aiogram.types.input_media_document import InputMediaDocument
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types.input_media_video import InputMediaVideo

from sqlalchemy import update
from sqlalchemy.future import select

from config.api_keys import CHANNEL_IDS
from config.api_keys import ADMINS
from core.keyboards.inline_keybords import subscribe_keyboard, go_to_bot_ikb
from config import messages
from database.models.send_post import SendPost


clean_time = None
logger = logging.getLogger(__name__)


class IsSubscribedMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = event.from_user.id
        chat_type = event.chat.type
        user_name = event.from_user.full_name
        
        if str(user_id) in ADMINS:
            return await handler(event, data)
        
        if event.text:
            if event.text.startswith('/start'):
                return await handler(event, data)
        
        if chat_type != 'private' and event.photo:
            if event.caption!='/theme':
                return
                    
        
        checked_channels = []
        for channel_id in CHANNEL_IDS:
            try:
                member = await self.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            except Exception as e:
                logger.error(e)

            if member.status in ['member', 'creator', 'administrator']:
                continue
            
            else:
                checked_channels.append(channel_id)

        if not checked_channels:
            return await handler(event, data)
        
        else:
            if chat_type == 'private':
                await event.answer(text=messages.MESSAGE_YOU_NOT_SUBSCRIBE,
                                        reply_markup=subscribe_keyboard(checked_channels))
            else:
                await event.answer(text=f'{user_name}{messages.MESSAGE_YOU_NOT_SUBSCRIBE_GROUP}',
                                   reply_markup=go_to_bot_ikb())


class PostSenderMiddleware(BaseMiddleware):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        session = data['session']
        db_sender: SendPost = data['post_data']
        send_post = db_sender.send_post
        
        if send_post:
            user = event.chat.id
            with open('POST_DATA.json', 'r') as file:
                post_data = json.load(file)
                
            count = db_sender.user_count
            if count <=0:
                await session.execute(update(SendPost).where(SendPost.id==db_sender.id)
                                    .values(
                                        send_post=False,
                                        user_count=0,
                                        user_list=[]
                                    ))
                await session.commit()
                    
                return await handler(event, data)
            
            users = db_sender.user_list
            key = post_data['key']
            if user not in users and key:
                if key == 'message':
                    load_message = Message.model_validate_json(post_data[key])
                    
                    if load_message.caption:
                        caption = load_message.caption
                    else:
                        caption = load_message.caption
                        
                    await self.bot.copy_message(
                        chat_id=user,
                        from_chat_id=load_message.chat.id,
                        message_id=load_message.message_id,
                        caption=caption,
                        caption_entities=load_message.caption_entities,
                        reply_markup=load_message.reply_markup
                    )
                else:
                    data_list = post_data[key]
                    media = []
                    for i in data_list:
                        if 'photo' in i.keys():
                            if i['photo']['caption']:
                                caption = i['photo']['caption']
                            else:
                                caption = i['photo']['caption']
                            post_part = InputMediaPhoto(
                                media=i['photo']['file_id'],
                                caption=caption,
                                caption_entities=i['photo']['caption_entities'],
                            )
                            media.append(post_part)
                            continue
                        elif 'video' in i.keys():
                            if i['video']['caption']:
                                caption = i['video']['caption']
                            else:
                                caption = i['video']['caption']
                            post_part = InputMediaVideo(
                                media=i['video']['file_id'],
                                caption=caption,
                                caption_entities=i['video']['caption_entities'],
                            )
                            media.append(post_part)
                            continue
                        elif 'audio' in i.keys():
                            if i['audio']['caption']:
                                caption = i['audio']['caption']
                            else:
                                caption = i['audio']['caption']
                            post_part = InputMediaAudio(
                                media=i['audio']['file_id'],
                                caption=caption,
                                caption_entities=i['audio']['caption_entities'],
                            )
                            media.append(post_part)
                            continue
                        elif 'animation' in i.keys():
                            if i['animation']['caption']:
                                caption = i['animation']['caption']
                            else:
                                caption = i['animation']['caption']
                            post_part = InputMediaAnimation(
                                media=i['animation']['file_id'],
                                caption=caption,
                                caption_entities=i['animation']['caption_entities'],
                            )
                            media.append(post_part)
                            continue
                        elif 'document' in i.keys():
                            if i['document']['caption']:
                                caption = i['document']['caption']
                            else:
                                caption = i['document']['caption']
                            post_part = InputMediaDocument(
                                media=i['document']['file_id'],
                                caption=caption,
                                caption_entities=i['document']['caption_entities'],
                            )
                            media.append(post_part)
                    
                    await event.answer_media_group(media=media)
            
                user_list = list(db_sender.user_list)
                user_list.append(user)
                
                await session.execute(update(SendPost).where(SendPost.id==db_sender.id)
                                    .values(
                                        user_count=db_sender.user_count-1,
                                        user_list=user_list
                                    ))
                await session.commit()
                
                post_db = await session.scalar(select(SendPost))
                data['post_data'] = post_db
                
                
        
        return await handler(event, data)


class CleanupMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if clean_time:
            current_time = datetime.now()
            time_difference = current_time - clean_time
            
            if time_difference.total_seconds() >= 0:
                await check_and_delete_files()
            
        return await handler(event, data)
    

async def check_and_delete_files():
    global clean_time
    download_photo_folder = 'download_photo'
    gener_image_folder = 'gener_image'

    # Перевіряємо наявність папок
    if not os.path.exists(download_photo_folder) or not os.path.exists(gener_image_folder):
        return

    # Ініціалізуємо список для зберігання шляхів до файлів, які потрібно видалити
    files_to_delete = []

    # Перевіряємо файли в папці download_photo
    for filename in os.listdir(download_photo_folder):
        file_path = os.path.join(download_photo_folder, filename)
        if os.path.isfile(file_path):
            files_to_delete.append(file_path)

    # Перевіряємо файли в папці gener_image
    for filename in os.listdir(gener_image_folder):
        file_path = os.path.join(gener_image_folder, filename)
        if os.path.isfile(file_path):
            files_to_delete.append(file_path)

    # Перевіряємо, чи є файли для видалення
    if files_to_delete:
        # Видаляємо файли зі списку
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {str(e)}")
        print('Folders cleaned.')
    
    current_datetime = datetime.now()
    # Додаємо один день до дати
    new_date = current_datetime + timedelta(days=1)
    # Встановлюємо час на 3:00 години ночі
    new_time = time(3, 0, 0)
    # Поєднуємо нову дату та час в один об'єкт datetime
    clean_time = datetime.combine(new_date, new_time)
    
