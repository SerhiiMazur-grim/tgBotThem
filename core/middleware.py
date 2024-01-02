from datetime import datetime, timedelta, time
import os
from typing import Callable, Awaitable, Dict, Any
import json

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from aiogram.types.input_media_animation import InputMediaAnimation
from aiogram.types.input_media_document import InputMediaDocument
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types.input_media_video import InputMediaVideo


clean_time = None


class PostSenderMiddleware(BaseMiddleware):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        with open('SEND_POST.json', 'r') as file:
            send_post = json.load(file)
        if send_post['send_post']:
            user = event.chat.id
            with open('POST_DATA.json', 'r') as file:
                post_data = json.load(file)
                
            count = post_data['count']
            if count <=0:
                with open('SEND_POST.json', 'w') as file:
                    send_post['send_post'] = False
                    json.dump(send_post, file, indent=4)
                    
                return await handler(event, data)
            
            users = post_data['users']
            key = post_data['key']
            if user not in users and key:
                if key == 'text':
                        await event.answer(text=post_data[key] if not post_data[key].startswith('POST\n') else post_data[key][5:])
                elif key == 'message':
                    load_message = Message.model_validate_json(post_data[key])
                    
                    if load_message.caption:
                        caption = load_message.caption if not load_message.caption.startswith('POST\n') else load_message.caption[5:]
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
                                caption = i['photo']['caption'] if not i['photo']['caption'].startswith('POST\n') else i['photo']['caption'][5:]
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
                                caption = i['video']['caption'] if not i['video']['caption'].startswith('POST\n') else i['video']['caption'][5:]
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
                                caption = i['audio']['caption'] if not i['audio']['caption'].startswith('POST\n') else i['audio']['caption'][5:]
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
                                caption = i['animation']['caption'] if not i['animation']['caption'].startswith('POST\n') else i['animation']['caption'][5:]
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
                                caption = i['document']['caption'] if not i['document']['caption'].startswith('POST\n') else i['document']['caption'][5:]
                            else:
                                caption = i['document']['caption']
                            post_part = InputMediaDocument(
                                media=i['document']['file_id'],
                                caption=caption,
                                caption_entities=i['document']['caption_entities'],
                            )
                            media.append(post_part)
                    
                    await event.answer_media_group(media=media)
            
                post_data['users'].append(user)
                post_data['count'] -= 1
                with open('POST_DATA.json', 'w') as file:
                    json.dump(post_data, file, indent=4)
                
                
        
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
    
