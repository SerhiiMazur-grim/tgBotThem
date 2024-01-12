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


async def handler_abort(callback_query: CallbackQuery, bot: Bot):
    """ бробник натискання на кнопку відміни """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        await callback_query.message.delete()
        await dell_data(user_data=USER_DATA, chat_id=chat_id)
        USER_DATA[chat_id] = {}
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handle_photo(message: Message, bot: Bot):
    """ Отримуємо фото від користувача та оброблємо його """
    
    if message.media_group_id:
        return
    
    chat_id = message.chat.id
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
    USER_DATA[chat_id] = {}
    USER_DATA[chat_id]['user_id'] = message.from_user.id
    USER_DATA[chat_id]['sended_photo'] = message

    photo_id = photo.file_id
    get_photo = await bot.get_file(photo_id)

    new_filename = f"{photo_id}.{get_photo.file_path.split('.')[-1]}"
    USER_DATA[chat_id]['image_name'] = new_filename
    download_file = os.path.join('download_photo', new_filename)
    await bot.download_file(file_path=get_photo.file_path, destination=download_file)

    try:
        colors = await image_color_picker(download_file)
    except:
        await wait_message.delete()
        await message.reply(text=messages.NOT_IMAGE)
        
    USER_DATA[chat_id]['colors'] = colors
    color_pick_image = f'{photo_id}{message.from_user.id}.jpg'
    USER_DATA[chat_id]['colors_image'] = color_pick_image
    await create_image(USER_DATA[chat_id]['colors'], color_pick_image)

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
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        device = callback_query.data.split('_')[-1]
        USER_DATA[chat_id]['device'] = device

        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
            reply_markup=inline_keybords.choose_background_color_keyboard(USER_DATA[chat_id]['colors'])
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_back_to_device_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору девайса """
    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_DEVICE_TEXT,
            reply_markup=inline_keybords.choose_device_keyboard()
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_background_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору кольору фону """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        color = callback_query.data.split('_')[-1]
        USER_DATA[chat_id]['background_color'] = color

        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
            reply_markup=inline_keybords.choose_primary_text_color_keyboard(USER_DATA[chat_id]['colors'])
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_back_to_background_color_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору кольору фону """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
            reply_markup=inline_keybords.choose_background_color_keyboard(USER_DATA[chat_id]['colors'])
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_primary_text_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        color = callback_query.data.split('_')[-1]
        bg_color = USER_DATA[chat_id]['background_color']
        if color == bg_color:
            await callback_query.answer(
                text='Колір фону не повинен бути однаковим з кольорм основного тексту!'
            )
            return
            
        USER_DATA[chat_id]['primary_text_color'] = color

        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
            reply_markup=inline_keybords.choose_secondary_text_color_keyboard(USER_DATA[chat_id]['colors'])
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_back_to_primary_text_color_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
            reply_markup=inline_keybords.choose_primary_text_color_keyboard(USER_DATA[chat_id]['colors'])
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_secondary_text_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        color = callback_query.data.split('_')[-1]
        USER_DATA[chat_id]['secondary_text_color'] = color

        if USER_DATA[chat_id]['device'] != 'iphone':
            await callback_query.message.edit_caption(
                caption=messages.CHOOSE_ALFA,
                reply_markup=inline_keybords.choose_alfa_background_color_keyboard()
            )
        else:
            theme = await create_theme(USER_DATA[chat_id], chat_id)
            await callback_query.message.delete()
            await USER_DATA[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme),
                                                                    caption=messages.MESSAGE_THEME_DONE)
            await dell_data(user_data=USER_DATA, chat_id=chat_id)
            USER_DATA[chat_id] = {}
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_back_to_secondary_text_color_choose(callback_query: CallbackQuery, bot: Bot):
    """ Обробник повернення до вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        await callback_query.message.edit_caption(
            caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
            reply_markup=inline_keybords.choose_secondary_text_color_keyboard(USER_DATA[chat_id]['colors'])
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_alfa_background_color(callback_query: CallbackQuery, bot: Bot):
    """ Обробник вибору прозорості для повідомлення """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        if USER_DATA[chat_id]['device'] != 'iphone':
            background_alfa = callback_query.data.split('_')[-1]
            USER_DATA[chat_id]['background_alfa'] = background_alfa

            theme = await create_theme(USER_DATA[chat_id], chat_id)
            await callback_query.message.delete()
            await USER_DATA[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme),
                                                                    caption=messages.MESSAGE_THEME_DONE)
            await dell_data(user_data=USER_DATA, chat_id=chat_id)
            USER_DATA[chat_id] = {}
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )


async def handler_auto_theme(callback_query: CallbackQuery, bot: Bot):
    """ Обробник автоматичного вибору кольору для теми """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['user_id'] == callback_query.from_user.id:
        if USER_DATA[chat_id]['device'] == 'android':

            USER_DATA[chat_id]['background_color'] = USER_DATA[chat_id]['colors'][0]
            USER_DATA[chat_id]['primary_text_color'] = USER_DATA[chat_id]['colors'][4]
            USER_DATA[chat_id]['secondary_text_color'] = USER_DATA[chat_id]['colors'][3]
            USER_DATA[chat_id]['background_alfa'] = 'a20'

            theme = await create_theme(USER_DATA[chat_id], chat_id)
            await callback_query.message.delete()
            await USER_DATA[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme),
                                                                    caption=messages.MESSAGE_THEME_DONE)
            await dell_data(user_data=USER_DATA, chat_id=chat_id)
            USER_DATA[chat_id] = {}

        elif USER_DATA[chat_id]['device'] == 'iphone':

            USER_DATA[chat_id]['background_color'] = USER_DATA[chat_id]['colors'][0]
            USER_DATA[chat_id]['primary_text_color'] = USER_DATA[chat_id]['colors'][4]
            USER_DATA[chat_id]['secondary_text_color'] = USER_DATA[chat_id]['colors'][3]

            theme = await create_theme(USER_DATA[chat_id], chat_id)
            await callback_query.message.delete()
            await USER_DATA[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme),
                                                                    caption=messages.MESSAGE_THEME_DONE)
            await dell_data(user_data=USER_DATA, chat_id=chat_id)
            USER_DATA[chat_id] = {}

        elif USER_DATA[chat_id]['device'] == 'desktop':

            USER_DATA[chat_id]['background_color'] = USER_DATA[chat_id]['colors'][0]
            USER_DATA[chat_id]['primary_text_color'] = USER_DATA[chat_id]['colors'][4]
            USER_DATA[chat_id]['secondary_text_color'] = USER_DATA[chat_id]['colors'][3]
            USER_DATA[chat_id]['background_alfa'] = 'a20'

            theme = await create_theme(USER_DATA[chat_id], chat_id)
            await callback_query.message.delete()
            await USER_DATA[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme),
                                                                    caption=messages.MESSAGE_THEME_DONE)
            await dell_data(user_data=USER_DATA, chat_id=chat_id)
            USER_DATA[chat_id] = {}
    else:
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=messages.MESSAGE_IS_NOT_YOUR_THEME,
            show_alert=True
        )
