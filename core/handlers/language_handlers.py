from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto

from config import messages
from core.utils import is_user_subscribed, is_private_chat
from core.keyboards.reply_keybords import nex_languages_keyboard, user_keyboard
from core.keyboards.inline_keybords import choice_device_lang_get_ikb, choice_category_lang_db_get_ikb
from core.database import get_languages_from_catalog


USER_QUERY = {}
USER_LANGUAGE_CATALOG = {}


async def get_catalog_languages(message: Message, bot: Bot):
    user_id = message.from_user.id
    if await is_user_subscribed(message, bot) and is_private_chat(message):
        USER_QUERY[user_id] = {}
        USER_LANGUAGE_CATALOG[user_id] = {}
        await message.delete()
        await message.answer(text=messages.MESSAGE_CHOICE_DEVICE_FOR_LANG,
                             reply_markup=choice_device_lang_get_ikb())


async def get_device_catalog_languages(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    USER_QUERY[user_id]['device'] = callback_query.data.split('_')[-1]
    
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                            reply_markup=choice_category_lang_db_get_ikb())
    

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
    if await is_user_subscribed(message, bot) and is_private_chat(message):
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
