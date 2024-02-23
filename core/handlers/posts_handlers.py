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

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, update

from config import messages
from core.keyboards.inline_keybords import send_post_ikb, start_create_post_ikb, send_limited_post_ikb, \
    abort_sending_limited_post_ikb
from core.handlers.basic import bot_is_blocked
from core.states import AddPostState
from core.mailer import MessageMailer, GroupMessageMailer
from database.models.user import User
from database.models.send_post import SendPost


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
        await data['post'].send_copy(chat_id=message.chat.id, reply_markup=data['post'].reply_markup)
        
        await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())


async def view_post(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    
    if not data:
        await message.answer(text=messages.MESSAGE_NO_POST)
        return
    
    post_type = data['post_type']
    
    if post_type == 'media':
        await data['post'].send_copy(chat_id=message.chat.id, reply_markup=data['post'].reply_markup)
        await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())
        
    else:
        media_list = await get_media_group_list(data)
        
        await message.answer_media_group(media=media_list)
        await message.answer(text=messages.MESSAGE_IS_YOUR_POST, reply_markup=send_post_ikb())


async def send_post_to_all(callback_query: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    data = await state.get_data()
    await state.clear()
    
    chats = (await session.scalars(select(User.id).where(User.active==True))).all()
    
    post_type = data['post_type']
    
    if data:
        await callback_query.message.delete()
        m = await callback_query.message.answer(text=messages.MESSAGE_POST_IS_SEND)
        
        if post_type == 'media':
            await MessageMailer.start_mailing(data['post'], chats, session)
        else:
            media = await get_media_group_list(data)
            await GroupMessageMailer.start_mailing(m, bot, media, chats, session)
        
    #     for chat in chats:
    #         if post_type == 'media':
    #             try:
    #                 await data['post'].send_copy(chat_id=chat)
    #             except Exception as err:
    #                 await bot_is_blocked(err, session, chat)
                    
    #         else:
    #             media = await get_media_group_list(data)
    #             try:
    #                 await bot.send_media_group(chat_id=chat, media=media)
    #             except Exception as err:
    #                 await bot_is_blocked(err, session, chat)
                    
    #     await callback_query.message.answer(text=messages.MESSAGE_POST_SEND_COMPLITE)
    else:
        await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_private(callback_query: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    data = await state.get_data()
    await state.clear()
    chats = (await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type=='private'
    )))).all()
    post_type = data['post_type']
    
    if data:
        await callback_query.message.delete()
        m = await callback_query.message.answer(text=messages.MESSAGE_POST_IS_SEND)
        
        if post_type == 'media':
            await MessageMailer.start_mailing(data['post'], chats, session)
        else:
            media = await get_media_group_list(data)
            await GroupMessageMailer.start_mailing(m, bot, media, chats, session)
        
        # for chat in chats:
        #     if post_type == 'media':
        #         try:
        #             await data['post'].send_copy(chat_id=chat)
        #         except Exception as err:
        #             await bot_is_blocked(err, session, chat)
        #     else:
        #         media = await get_media_group_list(data)
        #         try:
        #             await bot.send_media_group(chat_id=chat, media=media)
        #         except Exception as err:
        #             await bot_is_blocked(err, session, chat)
                    
        # await callback_query.message.answer(text=messages.MESSAGE_POST_SEND_COMPLITE)
    else:
        await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def send_post_to_group(callback_query: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    data = await state.get_data()
    await state.clear()
    chats = (await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type!='private'
    )))).all()
    post_type = data['post_type']
    if data:
        await callback_query.message.delete()
        m = await callback_query.message.answer(text=messages.MESSAGE_POST_IS_SEND)
        
        if post_type == 'media':
            await MessageMailer.start_mailing(data['post'], chats, session)
        else:
            media = await get_media_group_list(data)
            await GroupMessageMailer.start_mailing(m, bot, media, chats, session)
        
        # for chat in chats:
        #     if post_type == 'media':
        #         try:
        #             await data['post'].send_copy(chat_id=chat)
        #         except Exception as err:
        #             await bot_is_blocked(err, session, chat)
        #     else:
        #         media = await get_media_group_list(data)
        #         try:
        #             await bot.send_media_group(chat_id=chat, media=media)
        #         except Exception as err:
        #             await bot_is_blocked(err, session, chat)
                    
        # await callback_query.message.answer(text=messages.MESSAGE_POST_SEND_COMPLITE)
    else:
        await callback_query.answer(text=messages.MESSAGE_NO_POST)


async def start_limited_post(callback_query: CallbackQuery, state: FSMContext, post_data: SendPost):
    await callback_query.answer()
    await callback_query.message.delete()
    send_post = post_data.send_post
    user_count = post_data.user_count
    if send_post:
        await callback_query.message.answer(text=f'{messages.MESSAGE_PREV_POST_NOT_SENDED}{user_count}',
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


async def send_limited_post(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
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
    }
    
    if post_type == 'media':
        json_data['key'] = 'message'
        json_data['message'] = post.model_dump_json()
                
    
    else:
        group_message = []
        for media in data['post']:
            if media.animation:
                if media.caption_entities:
                    cap = [i.model_dump_json() for i in media.caption_entities]
                else: cap = media.caption_entities
                dump_data = {'animation': {
                    'file_id': media.animation.file_id,
                    'caption': media.caption,
                    'caption_entities': cap
                }}
                group_message.append(dump_data)
                continue
            elif media.photo:
                if media.caption_entities:
                    cap = [i.model_dump_json() for i in media.caption_entities]
                else: cap = media.caption_entities
                dump_data = {'photo': {
                    'file_id': media.photo[-1].file_id,
                    'caption': media.caption,
                    'caption_entities': cap
                }}
                group_message.append(dump_data)
                continue
            elif media.video:
                if media.caption_entities:
                    cap = [i.model_dump_json() for i in media.caption_entities]
                else: cap = media.caption_entities
                dump_data = {'video': {
                    'file_id': media.video.file_id,
                    'caption': media.caption,
                    'caption_entities': cap
                }}
                group_message.append(dump_data)
                continue
            elif media.audio:
                if media.caption_entities:
                    cap = [i.model_dump_json() for i in media.caption_entities]
                else: cap = media.caption_entities
                dump_data = {'audio': {
                    'file_id': media.audio.file_id,
                    'caption': media.caption,
                    'caption_entities': cap
                }}
                group_message.append(dump_data)
                continue
            elif media.document:
                if media.caption_entities:
                    cap = [i.model_dump_json() for i in media.caption_entities]
                else: cap = media.caption_entities
                dump_data = {'document': {
                    'file_id': media.document.file_id,
                    'caption': media.caption,
                    'caption_entities': cap
                }}
                group_message.append(dump_data)
                continue
        
        json_data['key'] = 'group_message'
        json_data['group_message'] = group_message
            
    with open('POST_DATA.json', 'w') as file:
        json.dump(json_data, file, indent=4)
        
    post_db = await session.scalar(select(SendPost))
    await session.execute(update(SendPost).where(SendPost.id==post_db.id)
                          .values(
                              send_post=True,
                              user_count=int(users_count),
                              user_list=[]
                          ))
    await session.commit()
    
    await callback_query.message.answer(text=messages.MESSAGE_LIMITED_POST_SEND)
    
    
async def delete_post(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    current_state = await state.get_state()
    
    if current_state is not None:
        await state.clear()
        
    await callback_query.answer(text=messages.MESSAGE_DELETE_POST)


async def abort_create_post(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    current_state = await state.get_state()
        
    if current_state is not None:
        await state.clear()


async def abort_sending_limit_post(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    current_state = await state.get_state()
        
    if current_state is not None:
        await state.clear()

    
    with open('POST_DATA.json', 'w') as file:
        data = {
                "message": {},
                "group_message": [],
                "key": ""
            }   
        json.dump(data, file, indent=4)
    
    post_db = await session.scalar(select(SendPost))
    await session.execute(update(SendPost).where(SendPost.id==post_db.id)
                          .values(
                              send_post=False,
                              user_count=0,
                              user_list=[]
                          ))
    await session.commit()
    
    await callback_query.message.answer(text=messages.MESSAGE_SENDING_IS_STOP)
 
