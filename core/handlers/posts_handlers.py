import json

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types.input_media_animation import InputMediaAnimation
from aiogram.types.input_media_document import InputMediaDocument
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types.input_media_video import InputMediaVideo

from config import messages
from core.keyboards.inline_keybords import send_post_ikb, start_create_post_ikb, send_limited_post_ikb, abort_create_limited_post_ikb, \
    abort_sending_limited_post_ikb
from core.database import get_chats_id_from_db, get_private_chats_id_from_db, get_group_chats_id_from_db
from core.handlers.theme_handlers import handle_photo
from core.states import AddPostState


async def get_media_group_list(data: dict) -> list:
    media_list = []
    for post in data['post']:
        if post.photo:
            media = post.photo[-1].file_id
            caption = post.caption
            caption_entities = post.caption_entities
            photo = InputMediaPhoto(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(photo)
            continue
        
        elif post.video:
            media = post.video.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            video = InputMediaVideo(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(video)
            continue
        
        elif post.animation:
            media = post.animation.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]            
            animation = InputMediaAnimation(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(animation)
            continue

        elif post.document:
            media = post.document.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]
            document = InputMediaDocument(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(document)
            continue

        elif post.audio:
            media = post.audio.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            if caption != None:
                if caption.startswith('POST\n'):
                    caption = caption[5:]
            audio = InputMediaAudio(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(audio)
            continue
    return media_list


async def create_mailing(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(AddPostState.post)
    await message.answer(text=messages.MESSAGE_GIVE_ME_POST, parse_mode=ParseMode.HTML, reply_markup=start_create_post_ikb())


async def get_post(message: Message, state: FSMContext):
    group_post = message.media_group_id
    text = message.text
    caption = message.caption
    
    if text == messages.BUTTON_VIEW_MAILING:
        data = await state.get_data()
        await view_post(message, state)
        return
        
    if group_post:
        if caption:
            await state.update_data(post=[message])
            await state.update_data(post_type='group')
        else:
            data = await state.get_data()
            post = data['post']
            post.append(message)
            await state.update_data(post=post)
            
    else:
        await state.update_data(post=message)
        await state.update_data(post_type='media')
        data = await state.get_data()
        await data['post'].send_copy(chat_id=message.chat.id)
        
        await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())


async def view_post(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    
    if not data:
        await message.answer(text=messages.MESSAGE_NO_POST)
        return
    
    post_type = data['post_type']
    
    if post_type == 'media':
        await data['post'].send_copy(chat_id=message.chat.id)
        await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())
        
    else:
        media_list = await get_media_group_list(data)
        
        await message.answer_media_group(media=media_list)
        await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())


async def send_post_to_all(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    chats = await get_chats_id_from_db()
    post_type = data['post_type']
    if data:
        await callback_query.message.delete()
        await callback_query.message.answer(text=messages.MESSAGE_POST_IS_SEND)
        for chat in chats:
            if post_type == 'media':
                await data['post'].send_copy(chat_id=chat)
            else:
                media = await get_media_group_list(data)
                await bot.send_media_group(chat_id=chat, media=media)
    else:
        await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_private(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    chats = await get_private_chats_id_from_db()
    post_type = data['post_type']
    if data:
        await callback_query.message.delete()
        await callback_query.message.answer(text=messages.MESSAGE_POST_IS_SEND)
        for chat in chats:
            if post_type == 'media':
                await data['post'].send_copy(chat_id=chat)
            else:
                media = await get_media_group_list(data)
                await bot.send_media_group(chat_id=chat, media=media)
    else:
        await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_group(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    chats = await get_group_chats_id_from_db()
    post_type = data['post_type']
    if data:
        await callback_query.message.delete()
        await callback_query.message.answer(text=messages.MESSAGE_POST_IS_SEND)
        for chat in chats:
            if post_type == 'media':
                await data['post'].send_copy(chat_id=chat)
            else:
                media = await get_media_group_list(data)
                await bot.send_media_group(chat_id=chat, media=media)
    else:
        await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def start_limited_post(callback_query: CallbackQuery, state: FSMContext):
    with open('SEND_POST.json', 'r') as file:
        send_post = json.load(file)
    if send_post['send_post']:
        with open('POST_DATA.json', 'r') as file:
            data = json.load(file)
        await callback_query.message.answer(text=f'{messages.MESSAGE_PREV_POST_NOT_SENDED}{data["count"]}',
                                            reply_markup=abort_sending_limited_post_ikb())
    else:            
        await state.set_state(AddPostState.users_count)
        await callback_query.message.answer(text=messages.MESSAGE_SEND_USERS_COUNT)


async def get_users_count(message: Message, state: FSMContext):
    users_count = message.text
    try:
        users_count = int(users_count)
    except ValueError:
        await message.answer(text=messages.MESSAGE_IS_NOT_NUMBER)
        return
        
    await state.update_data(users_count=users_count)
    await message.answer(text=f'{messages.MESSAGE_USERS_COUNT_INSERT}{users_count}',
                         reply_markup=send_limited_post_ikb())


async def send_limited_post(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    data = await state.get_data()
    await state.clear()
    post_type = data['post_type']
    post = data['post']
    users_count = data['users_count']
    json_data = {
        "message": {},
        "group_message": [],
        "key": "",
        "count": int(users_count),
        "users": []
    }
    
    if post_type == 'media':
        json_data['key'] = 'message'
        json_data['message'] = post.model_dump_json()
                
    
    else:
        group_message = []
        for media in data['post']:
            if media.animation:
                dump_data = {'animation': {
                    'file_id': media.animation.file_id,
                    'caption': media.caption,
                    'caption_entities': media.caption_entities
                }}
                group_message.append(dump_data)
                continue
            elif media.photo:
                dump_data = {'photo': {
                    'file_id': media.photo[-1].file_id,
                    'caption': media.caption,
                    'caption_entities': media.caption_entities
                }}
                group_message.append(dump_data)
                continue
            elif media.video:
                dump_data = {'video': {
                    'file_id': media.video.file_id,
                    'caption': media.caption,
                    'caption_entities': media.caption_entities
                }}
                group_message.append(dump_data)
                continue
            elif media.audio:
                dump_data = {'audio': {
                    'file_id': media.audio.file_id,
                    'caption': media.caption,
                    'caption_entities': media.caption_entities
                }}
                group_message.append(dump_data)
                continue
            elif media.document:
                dump_data = {'document': {
                    'file_id': media.document.file_id,
                    'caption': media.caption,
                    'caption_entities': media.caption_entities
                }}
                group_message.append(dump_data)
                continue
        
        json_data['key'] = 'group_message'
        json_data['group_message'] = group_message
            
    with open('POST_DATA.json', 'w') as file:
        json.dump(json_data, file, indent=4)
        
    with open('SEND_POST.json', 'w') as file:
        json.dump({"send_post": True}, file, indent=4)
    
    await callback_query.message.answer(text=messages.MESSAGE_LIMITED_POST_SEND)
    
    
async def delete_post(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    current_state = await state.get_state()
    
    if current_state is not None:
        await state.clear()
        
    await callback_query.answer(text=messages.MESSAGE_DELETE_POST)


async def abort_create_post(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    current_state = await state.get_state()
        
    if current_state is not None:
        await state.clear()


async def abort_sending_limit_post(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
        
    if current_state is not None:
        await state.clear()
        
    with open('SEND_POST.json', 'w') as file:
            data = {"send_post": False}
            json.dump(data, file, indent=4)
    
    with open('POST_DATA.json', 'w') as file:
        data = {
                "message": {},
                "group_message": [],
                "key": "",
                "count": 0,
                "users": []
            }   
        json.dump(data, file, indent=4)
    await callback_query.message.answer(text=messages.MESSAGE_SENDING_IS_STOP)
 