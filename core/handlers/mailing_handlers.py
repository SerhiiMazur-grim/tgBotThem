import json

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
from core.keyboards.inline_keybords import send_post_ikb, start_create_post_ikb, send_limited_post_ikb, abort_create_limited_post_ikb, \
    abort_sending_limited_post_ikb
from core.database import get_chats_id_from_db, get_private_chats_id_from_db, get_group_chats_id_from_db


SEND_DATA = {}


async def create_mailing(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.delete()
        SEND_DATA[user_id] = {}
        SEND_DATA[user_id]['text'] = ''
        SEND_DATA[user_id]['self_group'] = []
        SEND_DATA[user_id]['forward'] = None
        SEND_DATA[user_id]['forward_group'] = []
        SEND_DATA[user_id]['key'] = ''
        SEND_DATA[user_id]['for_activ_users'] = False
        
        await message.answer(text=messages.MESSAGE_GIVE_ME_POST, parse_mode=ParseMode.HTML, reply_markup=start_create_post_ikb())


async def start_limited_post(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if is_admin(user_id) and SEND_DATA.get(user_id) != None:
        with open('SEND_POST.json', 'r') as file:
            send_post = json.load(file)
        if send_post['send_post']:
            with open('POST_DATA.json', 'r') as file:
                data = json.load(file)
            await callback_query.message.answer(text=f'{messages.MESSAGE_PREV_POST_NOT_SENDED}{data["count"]}',
                                                reply_markup=abort_sending_limited_post_ikb())
        else:            
            SEND_DATA[user_id]['for_activ_users'] = True
            await callback_query.message.answer(text=messages.MESSAGE_SEND_USERS_COUNT)


async def abort_sending_limit_post(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        with open('SEND_POST.json', 'w') as file:
                data = {"send_post": False}
                json.dump(data, file, indent=4)
        
        with open('POST_DATA.json', 'w') as file:
            data = {
                    "text": "",
                    "message": {},
                    "group_message": [],
                    "key": "",
                    "count": 0,
                    "users": []
                    
                }   
            json.dump(data, file, indent=4)
        await callback_query.message.answer(text=messages.MESSAGE_SENDING_IS_STOP)


async def init_limited_post(message: Message):
    user_id = message.from_user.id
    if is_admin(user_id) and SEND_DATA[user_id]['for_activ_users']:
        count = message.text.split(' ')[-1]
        data = {
                "text": "",
                "message": {},
                "group_message": [],
                "key": "",
                "count": int(count),
                "users": []
            }
        
        with open('POST_DATA.json', 'w') as file:
            json.dump(data, file, indent=4)
        await message.answer(text=f"{messages.MESSAGE_USERS_COUNT_INSERT}{count} {messages.MESSAGE_SEND_ME_POST_FOR_LIMIT_SENDS}",
                             reply_markup=abort_create_limited_post_ikb())


async def forward_post_message(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_admin(user_id) and SEND_DATA.get(user_id) != None:
        if SEND_DATA[user_id]['for_activ_users']:
            with open('POST_DATA.json', 'r') as file:
                data = json.load(file)
                
            data['message'] = message.model_dump_json()
            data['key'] = 'message'
            
            with open('POST_DATA.json', 'w') as file:
                json.dump(data, file, indent=4)
        else:    
            SEND_DATA[user_id]['forward'] = message
            SEND_DATA[user_id]['key'] = 'forward'
    


async def save_media_group_post_media(message: Message):
    user_id = message.from_user.id
    if is_admin(user_id) and SEND_DATA.get(user_id) != None:
        if SEND_DATA[user_id]['for_activ_users']:
            if message.text:
                with open('POST_DATA.json', 'r') as file:
                    data = json.load(file)
                
                data['text'] = message.text
                data['key'] = 'text'
                
                with open('POST_DATA.json', 'w') as file:
                    json.dump(data, file, indent=4)
                return
                    
            elif not message.media_group_id:
                with open('POST_DATA.json', 'r') as file:
                    data = json.load(file)
                
                data['message'] = message.model_dump_json()
                data['key'] = 'message'
                
                with open('POST_DATA.json', 'w') as file:
                    json.dump(data, file, indent=4)
                    
                return
            else:
                if message.animation:
                    dump_data = {'animation': {
                        'file_id': message.animation.file_id,
                        'caption': message.caption,
                        'caption_entities': message.caption_entities
                    }}
                elif message.photo:
                    dump_data = {'photo': {
                        'file_id': message.photo[-1].file_id,
                        'caption': message.caption,
                        'caption_entities': message.caption_entities
                    }}
                elif message.video:
                    dump_data = {'video': {
                        'file_id': message.video.file_id,
                        'caption': message.caption,
                        'caption_entities': message.caption_entities
                    }}
                elif message.audio:
                    dump_data = {'audio': {
                        'file_id': message.audio.file_id,
                        'caption': message.caption,
                        'caption_entities': message.caption_entities
                    }}
                elif message.document:
                    dump_data = {'document': {
                        'file_id': message.document.file_id,
                        'caption': message.caption,
                        'caption_entities': message.caption_entities
                    }}
                with open('POST_DATA.json', 'r') as file:
                    data = json.load(file)
                
                data['group_message'].append(dump_data)
                data['key'] = 'group_message'
                
                with open('POST_DATA.json', 'w') as file:
                    json.dump(data, file, indent=4)
                return
                
        else:
        
            if message.forward_from or message.forward_from_chat:
                key = 'forward_group'
            else: key = 'self_group'
            
            if message.text:
                text = message.text
                if text.startswith('POST\n'):
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
            for_active_users = SEND_DATA[user_id]['for_activ_users']
            if key and not for_active_users:
                if key == 'text':
                    await message.answer(text=SEND_DATA[user_id]['text'], reply_markup=send_post_ikb())
                    return
                elif key == 'forward':
                    await SEND_DATA[user_id]['forward'].send_copy(chat_id=message.chat.id)
                    await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())
                    return
                else:
                    await message.answer_media_group(media=SEND_DATA[user_id][key])
                    await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())
            else:
                with open('POST_DATA.json', 'r') as file:
                    data = json.load(file)
                key = data['key']
                if key:
                    if key == 'text':
                        await message.answer(text=data[key] if not data[key].startswith('POST\n') else data[key][5:])
                        await message.answer(text=f'Кількість юзерів яким буде відправлено цей пост: {data["count"]}',
                                             reply_markup=send_limited_post_ikb())
                    elif key == 'message':
                        load_message = Message.model_validate_json(data[key])
                        
                        if load_message.caption:
                            caption = load_message.caption if not load_message.caption.startswith('POST\n') else load_message.caption[5:]
                        else:
                            caption = load_message.caption
                            
                        await bot.copy_message(
                            chat_id=message.chat.id,
                            from_chat_id=load_message.chat.id,
                            message_id=load_message.message_id,
                            caption=caption,
                            caption_entities=load_message.caption_entities,
                            reply_markup=load_message.reply_markup
                        )
                        await message.answer(text=f'Кількість юзерів яким буде відправлено цей пост: {data["count"]}',
                                             reply_markup=send_limited_post_ikb())
                    else:
                        data_list = data[key]
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
                        
                        await message.answer_media_group(media=media)
                        await message.answer(text=f'Кількість юзерів яким буде відправлено цей пост: {data["count"]}',
                                             reply_markup=send_limited_post_ikb())
                        
                else:
                    await message.answer(text=messages.MESSAGE_NO_POST)
            
        else:
            await message.answer(text=messages.MESSAGE_NO_POST)


async def send_limited_post(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):  
        with open('POST_DATA.json', 'r') as file:
            post_data = json.load(file)
        key = post_data['key']
        if key:
            with open('SEND_POST.json', 'w') as file:
                data = {"send_post": True}
                json.dump(data, file, indent=4)
            await callback_query.message.answer(text=messages.MESSAGE_LIMITED_POST_SEND)
        else:
            await callback_query.message.answer(text=messages.MESSAGE_LIMITED_POST_NOT_SEND)


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
        if SEND_DATA[user_id]['for_activ_users']:
            data = {
                    "text": "",
                    "message": {},
                    "group_message": [],
                    "key": "",
                    "count": 0,
                    "users": []
                    
                }
            
            with open('POST_DATA.json', 'w') as file:
                json.dump(data, file, indent=4)
        SEND_DATA.pop(user_id)
        await callback_query.message.delete()
        await callback_query.answer(text=messages.MESSAGE_DELETE_POST)


async def abort_create_post(callback_query: CallbackQuery, bot: Bot):
    user_id = callback_query.from_user.id
    if is_admin(user_id):
        if SEND_DATA[user_id]['for_activ_users']:
            data = {
                    "text": "",
                    "message": {},
                    "group_message": [],
                    "key": "",
                    "count": 0,
                    "users": []
                    
                }
            
            with open('POST_DATA.json', 'w') as file:
                json.dump(data, file, indent=4)
        SEND_DATA.pop(user_id)
        await callback_query.message.delete()
