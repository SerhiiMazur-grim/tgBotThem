from aiogram import Bot
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums import ParseMode

from config import messages
from core.keyboards.reply_keybords import nex_languages_keyboard, user_keyboard
from core.keyboards import inline_keybords
from core.database import get_languages_from_catalog, add_language_to_catalog
from core.handlers.mailing_handlers import save_media_group_post_media


USER_QUERY = {}
USER_LANGUAGE_CATALOG = {}
ADMIN_ADD_LANGUAGE = {}


async def start_add_language(message: Message, bot: Bot):
    admin = message.from_user.id
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
    if ADMIN_ADD_LANGUAGE.get(admin):
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
    if ADMIN_ADD_LANGUAGE.get(admin):
        if ADMIN_ADD_LANGUAGE[admin]['init']:
            ADMIN_ADD_LANGUAGE[admin]['language']['category'] = callback_query.data.split('_')[-1]
            await callback_query.message.answer(text=messages.MESAGE_SEND_ME_PREVIEW_AND_TEXT, parse_mode=ParseMode.HTML)


async def add_previev_and_desc_for_language(message: Message, bot: Bot):
    admin = message.from_user.id
    if ADMIN_ADD_LANGUAGE.get(admin):
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
            if ADMIN_ADD_LANGUAGE.get(admin):
                if ADMIN_ADD_LANGUAGE[admin]['init']:
                    ADMIN_ADD_LANGUAGE[admin]['language']['preview'].append(message.photo[-1].file_id)
                if len(ADMIN_ADD_LANGUAGE[admin]['language']['preview']) == 3:
                    await save_language_to_db(message, admin)
                        
        else:
            await save_media_group_post_media(message)
    except:
        await save_media_group_post_media(message)


async def get_catalog_languages(message: Message, bot: Bot):
    user_id = message.from_user.id
    USER_QUERY[user_id] = {}
    USER_LANGUAGE_CATALOG[user_id] = {}
    await message.delete()
    await message.answer(text=messages.MESSAGE_CHOICE_DEVICE_FOR_LANG,
                            reply_markup=inline_keybords.choice_device_lang_get_ikb())


async def get_device_catalog_languages(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    USER_QUERY[user_id]['device'] = callback_query.data.split('_')[-1]
    
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                            reply_markup=inline_keybords.choice_category_lang_db_get_ikb())
    

async def get_category_catalog_themes(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    device = USER_QUERY[user_id]['device']
    category = callback_query.data.split('_')[-1]
    
    catalog = await get_languages_from_catalog(device, category)
    USER_LANGUAGE_CATALOG[user_id]['catalog'] = catalog
    USER_LANGUAGE_CATALOG[user_id]['start'] = 5
    USER_LANGUAGE_CATALOG[user_id]['end'] = 11
    
    if catalog:
        await callback_query.message.answer(text=messages.MESSAGE_OUR_LANGUAGES,
                                reply_markup=nex_languages_keyboard())
        for language in catalog[:5]:
            send_data = []
            for prewiew in language['preview']:
                if not send_data:
                    caption = language['description']
                else: caption = None
                send_data.append(InputMediaPhoto(
                    media=prewiew,
                    caption=caption
                ))
            await callback_query.message.answer_media_group(media=send_data)
    else:
        await callback_query.message.answer(text=messages.MESSAGE_NO_LANGUAGES_IN_CATALOG)


async def get_next_languages(message: Message, bot: Bot):
    user_id = message.from_user.id
    catalog = USER_LANGUAGE_CATALOG[user_id]['catalog']
    start = USER_LANGUAGE_CATALOG[user_id]['start']
    end = USER_LANGUAGE_CATALOG[user_id]['end']
    
    if catalog[start:end]: 
        for language in catalog[start:end]:
            send_data = []
            for prewiew in language['preview']:
                if not send_data:
                    caption = language['description']
                else: caption = None
                send_data.append(InputMediaPhoto(
                    media=prewiew,
                    caption=caption
                ))
            await message.answer_media_group(media=send_data)
        
        USER_LANGUAGE_CATALOG[user_id]['start'] += start
        USER_LANGUAGE_CATALOG[user_id]['end'] += end
    else:
        await message.delete()
        await message.answer(text=messages.MESSAGE_NO_MORE_LANGUAGES)


async def go_to_main_menu_from_lang_catalog(message: Message, bot: Bot):
    user_id = message.from_user.id
    USER_QUERY[user_id] = {}
    USER_LANGUAGE_CATALOG[user_id] = {}
    await message.delete()
    await message.answer(text=messages.BUTTON_BACK_FROM_LANG_CAT,
                            reply_markup=user_keyboard(user_id))
