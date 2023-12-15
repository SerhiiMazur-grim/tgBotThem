import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import messages
from core.handlers.basic import is_user_subscribed, dell_data
from core.image.gener_image import create_image
from core.image.image_analiz import image_color_picker
from core.keyboards.inline_keybords import choose_device_keyboard, choose_background_color_keyboard, \
    choose_primary_text_color_keyboard, choose_secondary_text_color_keyboard, choose_alfa_background_color_keyboard, \
    choice_category_ikb_keyboard, choice_device_db_ikb_keyboard
from core.theme_creator import create_theme
from config.api_keys import ADMINS
from core.database import add_theme_to_catalog


user_data = {}
ADMIN_ADD_DATA = {}


async def is_admin(user_id):
    return str(user_id) in ADMINS


async def start_add_theme(message: Message, bot: Bot):
    admin = message.from_user.id
    if await is_admin(admin):
        ADMIN_ADD_DATA[admin] = {'theme': {}}
        ADMIN_ADD_DATA[admin]['init'] = True
        await message.answer(text=messages.MESSAGE_CHOICE_DEVICE, reply_markup=choice_device_db_ikb_keyboard())


async def add_theme_device(callback_query: CallbackQuery):
    admin = callback_query.from_user.id
    if await is_admin(admin) and ADMIN_ADD_DATA.get(admin):
        if ADMIN_ADD_DATA[admin]['init']:
            ADMIN_ADD_DATA[admin]['theme']['device'] = callback_query.data.split('_')[-1]
            await callback_query.message.answer(text=messages.MESSAGE_SEND_PREVIEW_THEME)


async def handler_abort(callback_query: CallbackQuery, bot: Bot):
    """ бробник натискання на кнопку відміни """

    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    await dell_data(user_data=user_data, chat_id=chat_id)
    user_data[chat_id] = {}


async def handle_photo(message: Message, bot: Bot):
    """ Отримуємо фото від користувача та оброблємо його """
    
    admin = message.from_user.id
    if await is_admin(admin) and ADMIN_ADD_DATA.get(admin):
        if ADMIN_ADD_DATA[admin]['init'] and message.photo:
            preview = message.photo[-1]
            
            ADMIN_ADD_DATA[admin]['theme']['preview'] = preview.file_id
            await message.answer(text=messages.MESSAGE_SEND_THEME_FILE)
            return
            
        elif ADMIN_ADD_DATA[admin]['init'] and message.document:
            theme_file = message.document
            if theme_file.file_name.split('.')[-1] in ('attheme', 'tdesktop-theme', 'tgios-theme'):
                ADMIN_ADD_DATA[admin]['theme']['file'] = theme_file.file_id
                await message.answer(text=messages.MESSAGE_CHOICE_CATEGORY, reply_markup=choice_category_ikb_keyboard())
                return
            else:
                await message.answer(text=messages.MESSAGE_IS_NOT_THEME)
                return

    elif await is_user_subscribed(message, bot):
        if message.chat.type == 'private':
            if message.document:
                photo = message.document
                if photo.mime_type != 'image/jpeg':
                    await message.reply(text=messages.NOT_IMAGE)
                    return
                
            elif message.photo:
                photo = message.photo[-1]
                
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
        chat_id = message.chat.id
        user_data[chat_id] = {}
        user_data[chat_id]['sended_photo'] = message

        photo_id = photo.file_id
        get_photo = await bot.get_file(photo_id)

        new_filename = f"{photo_id}.{get_photo.file_path.split('.')[-1]}"  # Створити нове ім'я для збереження
        user_data[chat_id]['image_name'] = new_filename
        download_file = os.path.join('download_photo', new_filename)
        await bot.download_file(file_path=get_photo.file_path, destination=download_file)  # завантажити фото

        try:
            colors = await image_color_picker(download_file)
        except:
            await wait_message.delete()
            await message.reply(text=messages.NOT_IMAGE)
        user_data[chat_id]['colors'] = colors
        color_pick_image = f'{photo_id}{message.from_user.id}.jpg'
        user_data[chat_id]['colors_image'] = color_pick_image
        await create_image(user_data[chat_id]['colors'], color_pick_image)

        path = os.path.join('gener_image', color_pick_image)
        await wait_message.delete()
        await message.answer_photo(
            photo=FSInputFile(path=path),
            caption=messages.CHOOSE_DEVICE_TEXT,
            reply_markup=choose_device_keyboard()
        )


async def add_theme_category(callback_query: CallbackQuery):
    if ADMIN_ADD_DATA:
        admin = callback_query.from_user.id
        if await is_admin(admin) and ADMIN_ADD_DATA[admin]['init']:
            category = callback_query.data.split('_')[-1]
            preview = ADMIN_ADD_DATA[admin]['theme']['preview']
            theme = ADMIN_ADD_DATA[admin]['theme']['file']
            device = ADMIN_ADD_DATA[admin]['theme']['device']
            
            await add_theme_to_catalog(category, preview, theme, device)
            
            ADMIN_ADD_DATA[admin] = {}
            
            await callback_query.message.answer(text=messages.MESSAGE_ADDED_TO_DB)


async def handler_device(callback_query: CallbackQuery):
    """ Обробник вибору девайса """

    chat_id = callback_query.message.chat.id
    device = callback_query.data.split('_')[-1]
    user_data[chat_id]['device'] = device

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
        reply_markup=choose_background_color_keyboard(user_data[chat_id]['colors'])
    )


async def handler_back_to_device_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору девайса """

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_DEVICE_TEXT,
        reply_markup=choose_device_keyboard()
    )


async def handler_background_color(callback_query: CallbackQuery):
    """ Обробник вибору кольору фону """

    chat_id = callback_query.message.chat.id
    color = callback_query.data.split('_')[-1]
    user_data[chat_id]['background_color'] = color

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
        reply_markup=choose_primary_text_color_keyboard(user_data[chat_id]['colors'])
    )


async def handler_back_to_background_color_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору кольору фону """

    chat_id = callback_query.message.chat.id

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
        reply_markup=choose_background_color_keyboard(user_data[chat_id]['colors'])
    )


async def handler_primary_text_color(callback_query: CallbackQuery):
    """ Обробник вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id
    color = callback_query.data.split('_')[-1]
    user_data[chat_id]['primary_text_color'] = color

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
        reply_markup=choose_secondary_text_color_keyboard(user_data[chat_id]['colors'])
    )


async def handler_back_to_primary_text_color_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
        reply_markup=choose_primary_text_color_keyboard(user_data[chat_id]['colors'])
    )


async def handler_secondary_text_color(callback_query: CallbackQuery):
    """ Обробник вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id
    color = callback_query.data.split('_')[-1]
    user_data[chat_id]['secondary_text_color'] = color

    if user_data[chat_id]['device'] != 'iphone':
        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_ALFA,
            reply_markup=choose_alfa_background_color_keyboard()
        )
    else:
        theme = await create_theme(user_data[chat_id], chat_id)
        await callback_query.message.delete()
        await user_data[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme), caption=messages.MESSAGE_THEME_DONE)
        await dell_data(user_data=user_data, chat_id=chat_id)
        user_data[chat_id] = {}


async def handler_back_to_secondary_text_color_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
        reply_markup=choose_secondary_text_color_keyboard(user_data[chat_id]['colors'])
    )


async def handler_alfa_background_color(callback_query: CallbackQuery):
    """ Обробник вибору прозорості для повідомлення """

    chat_id = callback_query.message.chat.id
    if user_data[chat_id]['device'] != 'iphone':
        background_alfa = callback_query.data.split('_')[-1]
        user_data[chat_id]['background_alfa'] = background_alfa

        theme = await create_theme(user_data[chat_id], chat_id)
        await callback_query.message.delete()
        await user_data[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme), caption=messages.MESSAGE_THEME_DONE)
        await dell_data(user_data=user_data, chat_id=chat_id)
        user_data[chat_id] = {}


async def handler_auto_theme(callback_query: CallbackQuery):
    """ Обробник автоматичного вибору кольору для теми """

    chat_id = callback_query.message.chat.id
    if user_data[chat_id]['device'] == 'android':

        user_data[chat_id]['background_color'] = user_data[chat_id]['colors'][0]
        user_data[chat_id]['primary_text_color'] = user_data[chat_id]['colors'][4]
        user_data[chat_id]['secondary_text_color'] = user_data[chat_id]['colors'][3]
        user_data[chat_id]['background_alfa'] = 'a20'

        theme = await create_theme(user_data[chat_id], chat_id)
        await callback_query.message.delete()
        await user_data[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme), caption=messages.MESSAGE_THEME_DONE)
        await dell_data(user_data=user_data, chat_id=chat_id)
        user_data[chat_id] = {}

    elif user_data[chat_id]['device'] == 'iphone':

        user_data[chat_id]['background_color'] = user_data[chat_id]['colors'][0]
        user_data[chat_id]['primary_text_color'] = user_data[chat_id]['colors'][4]
        user_data[chat_id]['secondary_text_color'] = user_data[chat_id]['colors'][3]

        theme = await create_theme(user_data[chat_id], chat_id)
        await callback_query.message.delete()
        await user_data[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme), caption=messages.MESSAGE_THEME_DONE)
        await dell_data(user_data=user_data, chat_id=chat_id)
        user_data[chat_id] = {}

    elif user_data[chat_id]['device'] == 'desktop':

        user_data[chat_id]['background_color'] = user_data[chat_id]['colors'][0]
        user_data[chat_id]['primary_text_color'] = user_data[chat_id]['colors'][4]
        user_data[chat_id]['secondary_text_color'] = user_data[chat_id]['colors'][3]
        user_data[chat_id]['background_alfa'] = 'a20'

        theme = await create_theme(user_data[chat_id], chat_id)
        await callback_query.message.delete()
        await user_data[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme), caption=messages.MESSAGE_THEME_DONE)
        await dell_data(user_data=user_data, chat_id=chat_id)
        user_data[chat_id] = {}
