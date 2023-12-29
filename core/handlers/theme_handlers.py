import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, PollAnswer
from aiogram.enums import ParseMode

from config import messages
from core.handlers.basic import is_user_subscribed
from core.image.gener_image import create_image
from core.image.image_analiz import image_color_picker
from core.keyboards import inline_keybords
from core.keyboards.reply_keybords import user_keyboard
from core.theme_creator import create_theme
from core.database import add_theme_to_catalog, add_language_to_catalog
from core.utils import is_admin, dell_data, is_private_chat
from core.handlers.mailing_handlers import save_media_group_post_media


USER_DATA = {}
ADMIN_ADD_THEME = {}
ADMIN_ADD_LANGUAGE = {}


async def start_add_language(message: Message, bot: Bot):
    admin = message.from_user.id
    if is_admin(admin):
        await message.delete()
        ADMIN_ADD_LANGUAGE[admin] = {'language': {}}
        ADMIN_ADD_LANGUAGE[admin]['init'] = True
        await message.answer_poll(
            question=messages.MESSAGE_CHOICE_DEVICE_FOR_LANGUAGE,
            options=messages.DEVICE_FOR_LANGUAGE,
            is_anonymous=False,
            allows_multiple_answers=True
        )


async def add_language_device(poll: PollAnswer, bot: Bot):
    admin = poll.user.id
    if is_admin(admin) and ADMIN_ADD_LANGUAGE.get(admin):
        if ADMIN_ADD_LANGUAGE[admin]['init']:
            devices = [messages.DEVICE_FOR_LANGUAGE[i] for i in poll.option_ids]
            ADMIN_ADD_LANGUAGE[admin]['language']['devices'] = {
                'android': 'True' if 'android' in devices else 'False',
                'ios': 'True' if 'ios' in devices else 'False',
                'computer': 'True' if 'computer' in devices else 'False',
            }
            await bot.send_message(chat_id=poll.user.id,
                                   text=messages.MESSAGE_CHOICE_CATEGORY_FOR_LANGUAGE,
                                   reply_markup=inline_keybords.language_categories_ikb())


async def add_language_preview(callback_query: CallbackQuery):
    admin = callback_query.from_user.id
    if is_admin(admin) and ADMIN_ADD_LANGUAGE.get(admin):
        if ADMIN_ADD_LANGUAGE[admin]['init']:
            ADMIN_ADD_LANGUAGE[admin]['language']['category'] = callback_query.data.split('_')[-1]
            await callback_query.message.answer(text=messages.MESAGE_SEND_ME_PREVIEW_AND_TEXT, parse_mode=ParseMode.HTML)


async def add_previev_and_desc_for_language(message: Message, bot: Bot):
    admin = message.from_user.id
    if is_admin(admin) and ADMIN_ADD_LANGUAGE.get(admin):
        if ADMIN_ADD_LANGUAGE[admin]['init']:
            media_group_id = message.media_group_id
            preview = message.photo[-1].file_id
            description = message.caption[5:]
            ADMIN_ADD_LANGUAGE[admin]['language']['preview'] = [preview]
            ADMIN_ADD_LANGUAGE[admin]['language']['description'] = description
            ADMIN_ADD_LANGUAGE[admin]['media_group_id'] = media_group_id


async def save_language_to_db(message, admin):
    android = ADMIN_ADD_LANGUAGE[admin]['language']['devices']['android']
    ios = ADMIN_ADD_LANGUAGE[admin]['language']['devices']['ios']
    computer = ADMIN_ADD_LANGUAGE[admin]['language']['devices']['computer']
    category = ADMIN_ADD_LANGUAGE[admin]['language']['category']
    preview = ', '.join(ADMIN_ADD_LANGUAGE[admin]['language']['preview'])
    description = ADMIN_ADD_LANGUAGE[admin]['language']['description']
    await add_language_to_catalog(
        android=android,
        ios=ios,
        computer=computer,
        category=category,
        preview=preview,
        description=description
    )
    await message.answer(text=messages.MESSAGE_LANGUAGE_IS_SAVE)


async def add_preview_for_language(message: Message, bot: Bot):
    admin = message.from_user.id
    media_group_id = message.media_group_id
    try:
        if ADMIN_ADD_LANGUAGE[admin]['media_group_id'] == media_group_id:
            if is_admin(admin) and ADMIN_ADD_LANGUAGE.get(admin):
                if ADMIN_ADD_LANGUAGE[admin]['init']:
                    ADMIN_ADD_LANGUAGE[admin]['language']['preview'].append(message.photo[-1].file_id)
                if len(ADMIN_ADD_LANGUAGE[admin]['language']['preview']) == 3:
                    await save_language_to_db(message, admin)
                        
        else:
            await save_media_group_post_media(message)
    except:
        await save_media_group_post_media(message)

        
async def start_add_theme(message: Message, bot: Bot):
    admin = message.from_user.id
    if is_admin(admin):
        await message.delete()
        ADMIN_ADD_THEME[admin] = {'theme': {}}
        ADMIN_ADD_THEME[admin]['init'] = True
        await message.answer(text=messages.MESSAGE_CHOICE_DEVICE,
                             reply_markup=inline_keybords.choice_device_db_ikb_keyboard())


async def abort_add_theme(callback_query: CallbackQuery):
    admin = callback_query.from_user.id
    if is_admin(admin) and ADMIN_ADD_THEME.get(admin):
        ADMIN_ADD_THEME[admin] = {}
        await callback_query.message.delete()


async def add_theme_device(callback_query: CallbackQuery):
    admin = callback_query.from_user.id
    if is_admin(admin) and ADMIN_ADD_THEME.get(admin):
        if ADMIN_ADD_THEME[admin]['init']:
            ADMIN_ADD_THEME[admin]['theme']['device'] = callback_query.data.split('_')[-1]
            await callback_query.message.answer(text=messages.MESSAGE_SEND_PREVIEW_THEME)


async def handler_abort(callback_query: CallbackQuery, bot: Bot):
    """ бробник натискання на кнопку відміни """

    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    await dell_data(user_data=USER_DATA, chat_id=chat_id)
    USER_DATA[chat_id] = {}


async def handle_photo(message: Message, bot: Bot):
    """ Отримуємо фото від користувача та оброблємо його """
    if message.media_group_id:
        return
    
    admin = message.from_user.id
    if is_admin(admin) and ADMIN_ADD_THEME.get(admin):
        if ADMIN_ADD_THEME[admin]['init'] and message.photo:
            preview = message.photo[-1]
            
            ADMIN_ADD_THEME[admin]['theme']['preview'] = preview.file_id
            await message.answer(text=messages.MESSAGE_SEND_THEME_FILE)
            return
            
        elif ADMIN_ADD_THEME[admin]['init'] and message.document:
            theme_file = message.document
            if theme_file.file_name.split('.')[-1] in ('attheme', 'tdesktop-theme', 'tgios-theme'):
                ADMIN_ADD_THEME[admin]['theme']['file'] = theme_file.file_id
                await message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                                     reply_markup=inline_keybords.choice_category_ikb_keyboard())
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
        chat_id = message.chat.id
        USER_DATA[chat_id] = {}
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


async def add_theme_category(callback_query: CallbackQuery):
    if ADMIN_ADD_THEME:
        admin = callback_query.from_user.id
        if is_admin(admin) and ADMIN_ADD_THEME[admin]['init']:
            category = callback_query.data.split('_')[-1]
            preview = ADMIN_ADD_THEME[admin]['theme']['preview']
            theme = ADMIN_ADD_THEME[admin]['theme']['file']
            device = ADMIN_ADD_THEME[admin]['theme']['device']
            
            await add_theme_to_catalog(category, preview, theme, device)
            
            ADMIN_ADD_THEME[admin] = {}
            
            await callback_query.message.answer(text=messages.MESSAGE_ADDED_TO_DB)


async def command_user_kb(message: Message, bot: Bot):
    user_id = message.from_user.id
    if is_private_chat(message) and is_admin(user_id):
        await message.delete()
        ADMIN_ADD_THEME[user_id] = {}
        
        await message.answer(text=messages.MESSAGE_ON_BACK_TO_USER_KB, reply_markup=user_keyboard(user_id))


async def handler_device(callback_query: CallbackQuery):
    """ Обробник вибору девайса """

    chat_id = callback_query.message.chat.id
    device = callback_query.data.split('_')[-1]
    USER_DATA[chat_id]['device'] = device

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
        reply_markup=inline_keybords.choose_background_color_keyboard(USER_DATA[chat_id]['colors'])
    )


async def handler_back_to_device_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору девайса """

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_DEVICE_TEXT,
        reply_markup=inline_keybords.choose_device_keyboard()
    )


async def handler_background_color(callback_query: CallbackQuery):
    """ Обробник вибору кольору фону """

    chat_id = callback_query.message.chat.id
    color = callback_query.data.split('_')[-1]
    USER_DATA[chat_id]['background_color'] = color

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
        reply_markup=inline_keybords.choose_primary_text_color_keyboard(USER_DATA[chat_id]['colors'])
    )


async def handler_back_to_background_color_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору кольору фону """

    chat_id = callback_query.message.chat.id

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_BACKGROUND_COLOR_TEXT,
        reply_markup=inline_keybords.choose_background_color_keyboard(USER_DATA[chat_id]['colors'])
    )


async def handler_primary_text_color(callback_query: CallbackQuery):
    """ Обробник вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id
    color = callback_query.data.split('_')[-1]
    USER_DATA[chat_id]['primary_text_color'] = color

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
        reply_markup=inline_keybords.choose_secondary_text_color_keyboard(USER_DATA[chat_id]['colors'])
    )


async def handler_back_to_primary_text_color_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору кольору основного тексту """

    chat_id = callback_query.message.chat.id

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_PRIMARY_COLOR_TEXT,
        reply_markup=inline_keybords.choose_primary_text_color_keyboard(USER_DATA[chat_id]['colors'])
    )


async def handler_secondary_text_color(callback_query: CallbackQuery):
    """ Обробник вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id
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


async def handler_back_to_secondary_text_color_choose(callback_query: CallbackQuery):
    """ Обробник повернення до вибору кольору не основного тексту """

    chat_id = callback_query.message.chat.id

    await callback_query.message.edit_caption(
        caption=messages.CHOOSE_SECONDARY_COLOR_TEXT,
        reply_markup=inline_keybords.choose_secondary_text_color_keyboard(USER_DATA[chat_id]['colors'])
    )


async def handler_alfa_background_color(callback_query: CallbackQuery):
    """ Обробник вибору прозорості для повідомлення """

    chat_id = callback_query.message.chat.id
    if USER_DATA[chat_id]['device'] != 'iphone':
        background_alfa = callback_query.data.split('_')[-1]
        USER_DATA[chat_id]['background_alfa'] = background_alfa

        theme = await create_theme(USER_DATA[chat_id], chat_id)
        await callback_query.message.delete()
        await USER_DATA[chat_id]['sended_photo'].reply_document(document=FSInputFile(path=theme),
                                                                caption=messages.MESSAGE_THEME_DONE)
        await dell_data(user_data=USER_DATA, chat_id=chat_id)
        USER_DATA[chat_id] = {}


async def handler_auto_theme(callback_query: CallbackQuery):
    """ Обробник автоматичного вибору кольору для теми """

    chat_id = callback_query.message.chat.id
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
