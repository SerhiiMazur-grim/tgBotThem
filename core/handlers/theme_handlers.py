import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import messages
from core.image.gener_image import create_image
from core.image.image_analiz import image_color_picker
from core.keyboards import inline_keybords
from core.theme_creator import create_theme
from core.utils import dell_data


USER_DATA = {}


async def theme_ikb_error(callback_query, bot):
    if callback_query.message.chat.type == 'private':
            # await callback_query.message.delete()
            await callback_query.message.answer(text=messages.MESSAGE_SOME_ERROR)
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_abort(callback_query: CallbackQuery, bot: Bot):
    """ бробник натискання на кнопку відміни """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    try:
        if USER_DATA[f'{chat_id}{user_id}']['user_id'] == callback_query.from_user.id:
            await callback_query.message.delete()
            await dell_data(user_data=USER_DATA, chat_id=f'{chat_id}{user_id}')
            USER_DATA[f'{chat_id}{user_id}'] = {}
    except:
        await theme_ikb_error(callback_query, bot)


async def handle_photo(message: Message, bot: Bot):
    """ Отримуємо фото від користувача та оброблємо його """
    
    if message.media_group_id:
        return
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    key = f'{chat_id}{user_id}'
    if message.chat.type == 'private':
        
        if message.document:
            photo = message.document
            if photo.mime_type != 'image/jpeg':
                await message.reply(text=messages.NOT_IMAGE)
                return
            
        elif message.photo:
            photo = message.photo[-1]
        else: return
            
    elif message.chat.type != 'private' and message.caption == '/theme':
        if message.document:
            photo = message.document
            if photo.mime_type != 'image/jpeg':
                await message.reply(text=messages.NOT_IMAGE)
                return
            
        elif message.photo:
            photo = message.photo[-1]
    else:
        return
    
    wait_message = await message.answer(text=messages.WAIT_MESSAGE)
    USER_DATA[key] = {}
    USER_DATA[key]['user_id'] = message.from_user.id
    USER_DATA[key]['sended_photo'] = message

    photo_id = photo.file_id
    get_photo = await bot.get_file(photo_id)

    new_filename = f"{photo_id}.{get_photo.file_path.split('.')[-1]}"
    USER_DATA[key]['image_name'] = new_filename
    download_file = os.path.join('download_photo', new_filename)
    await bot.download_file(file_path=get_photo.file_path, destination=download_file)

    try:
        colors = await image_color_picker(download_file)
    except:
        await wait_message.delete()
        await message.reply(text=messages.NOT_IMAGE)
        
    USER_DATA[key]['colors'] = colors
    color_pick_image = f'{photo_id}{message.from_user.id}.jpg'
    USER_DATA[key]['colors_image'] = color_pick_image
    await create_image(USER_DATA[key]['colors'], color_pick_image)

    path = os.path.join('gener_image', color_pick_image)
    await wait_message.delete()
    await message.answer_photo(
        photo=FSInputFile(path=path),
        caption=messages.CHOOSE_DEVICE_TEXT,
        reply_markup=inline_keybords.choose_device_keyboard()
    )


async def handler_device(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору девайса """
    
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try: 
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            device = callback_query.data.split('_')[-1]
            USER_DATA[key]['device'] = device

            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
                reply_markup=inline_keybords.choose_background_color_keyboard(USER_DATA[key]['colors'])
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_back_to_device_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору девайса """
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_DEVICE_TEXT,
                reply_markup=inline_keybords.choose_device_keyboard()
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_background_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору кольору фону """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            color = callback_query.data.split('_')[-1]
            USER_DATA[key]['background_color'] = color

            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
                reply_markup=inline_keybords.choose_primary_text_color_keyboard(USER_DATA[key]['colors'])
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_back_to_background_color_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору кольору фону """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
                reply_markup=inline_keybords.choose_background_color_keyboard(USER_DATA[key]['colors'])
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_primary_text_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            color = callback_query.data.split('_')[-1]
            bg_color = USER_DATA[key]['background_color']
            if color == bg_color:
                await callback_query.answer(
                    text=messages.MESSAGE_EQUAL_COLOR_1
                )
                return
                
            USER_DATA[key]['primary_text_color'] = color

            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
                reply_markup=inline_keybords.choose_secondary_text_color_keyboard(USER_DATA[key]['colors'])
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_back_to_primary_text_color_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
                reply_markup=inline_keybords.choose_primary_text_color_keyboard(USER_DATA[key]['colors'])
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_secondary_text_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            color = callback_query.data.split('_')[-1]
            bg_color = USER_DATA[key]['background_color']
            if color == bg_color:
                await callback_query.answer(
                    text=messages.MESSAGE_EQUAL_COLOR_2
                )
                return
            
            USER_DATA[key]['secondary_text_color'] = color

            if USER_DATA[key]['device'] != 'iphone':
                await callback_query.message.edit_caption(
                    caption=messages.CHOOSE_ALFA,
                    reply_markup=inline_keybords.choose_alfa_background_color_keyboard()
                )
            else:
                await callback_query.message.delete()
                wait_message = await callback_query.message.answer(text=messages.MESSAGE_CREATING_THEME)
                theme, preview = await create_theme(USER_DATA[key], key)
                
                await wait_message.delete()
                await callback_query.message.answer_photo(photo=FSInputFile(path=preview))
                await callback_query.message.answer_document(document=FSInputFile(path=theme),
                                                                        caption=messages.MESSAGE_THEME_DONE)
                await dell_data(user_data=USER_DATA, chat_id=key)
                USER_DATA[key] = {}
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_back_to_secondary_text_color_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
                reply_markup=inline_keybords.choose_secondary_text_color_keyboard(USER_DATA[key]['colors'])
            )
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_alfa_background_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору прозорості для повідомлення """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            if USER_DATA[key]['device'] != 'iphone':
                background_alfa = callback_query.data.split('_')[-1]
                USER_DATA[key]['background_alfa'] = background_alfa

                await callback_query.message.delete()
                wait_message = await callback_query.message.answer(text=messages.MESSAGE_CREATING_THEME)
                
                theme, preview = await create_theme(USER_DATA[key], key)
                
                await wait_message.delete()
                await callback_query.message.answer_photo(photo=FSInputFile(path=preview))
                await callback_query.message.answer_document(document=FSInputFile(path=theme),
                                                                        caption=messages.MESSAGE_THEME_DONE)
                
                await dell_data(user_data=USER_DATA, chat_id=key)
                USER_DATA[key] = {}
    except:
        await theme_ikb_error(callback_query, bot)


async def handler_auto_theme(callback_query: CallbackQuery, bot: Bot):
    """ Обробник автоматичного вибору кольору для теми """

    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    key = f'{chat_id}{user_id}'
    try:
        if USER_DATA[key]['user_id'] == callback_query.from_user.id:
            if USER_DATA[key]['device'] == 'android':

                USER_DATA[key]['background_color'] = USER_DATA[key]['colors'][0]
                USER_DATA[key]['primary_text_color'] = USER_DATA[key]['colors'][4]
                USER_DATA[key]['secondary_text_color'] = USER_DATA[key]['colors'][3]
                USER_DATA[key]['background_alfa'] = 'a20'

                await callback_query.message.delete()
                wait_message = await callback_query.message.answer(text=messages.MESSAGE_CREATING_THEME)
                theme, preview = await create_theme(USER_DATA[key], key)
                
                await wait_message.delete()
                await callback_query.message.answer_photo(photo=FSInputFile(path=preview))
                await callback_query.message.answer_document(document=FSInputFile(path=theme),
                                                                        caption=messages.MESSAGE_THEME_DONE)
                

            elif USER_DATA[key]['device'] == 'iphone':

                USER_DATA[key]['background_color'] = USER_DATA[key]['colors'][0]
                USER_DATA[key]['primary_text_color'] = USER_DATA[key]['colors'][4]
                USER_DATA[key]['secondary_text_color'] = USER_DATA[key]['colors'][3]

                await callback_query.message.delete()
                wait_message = await callback_query.message.answer(text=messages.MESSAGE_CREATING_THEME)
                theme, preview = await create_theme(USER_DATA[key], key)
                
                await wait_message.delete()
                await callback_query.message.answer_photo(photo=FSInputFile(path=preview))
                await callback_query.message.answer_document(document=FSInputFile(path=theme),
                                                                        caption=messages.MESSAGE_THEME_DONE)

            elif USER_DATA[key]['device'] == 'desktop':

                USER_DATA[key]['background_color'] = USER_DATA[key]['colors'][0]
                USER_DATA[key]['primary_text_color'] = USER_DATA[key]['colors'][4]
                USER_DATA[key]['secondary_text_color'] = USER_DATA[key]['colors'][3]
                USER_DATA[key]['background_alfa'] = 'a20'

                await callback_query.message.delete()
                wait_message = await callback_query.message.answer(text=messages.MESSAGE_CREATING_THEME)
                theme, preview = await create_theme(USER_DATA[key], key)
                await wait_message.delete()
                await callback_query.message.answer_photo(photo=FSInputFile(path=preview))
                await callback_query.message.answer_document(document=FSInputFile(path=theme),
                                                                        caption=messages.MESSAGE_THEME_DONE)
                
            await dell_data(user_data=USER_DATA, chat_id=key)
            USER_DATA[key] = {}
    except:
        await theme_ikb_error(callback_query, bot)