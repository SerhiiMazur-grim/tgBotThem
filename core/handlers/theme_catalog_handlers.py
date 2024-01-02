from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from config import messages
from core.utils import is_user_subscribed, is_private_chat
from core.keyboards.inline_keybords import choice_device_db_get_ikb, choice_category_db_get_ikb
from core.keyboards.reply_keybords import nex_themes_keyboard, user_keyboard
from core.database import get_themes_from_catalog


USER_QUERY = {}
USER_THEME_CATALOG = {}


async def get_catalog_themes(message: Message, bot: Bot):
    user_id = message.from_user.id
    if await is_user_subscribed(message, bot) and is_private_chat(message):
        USER_QUERY[user_id] = {}
        await message.delete()
        await message.answer(text=messages.MESSAGE_CHOICE_DEVICE,
                             reply_markup=choice_device_db_get_ikb())


async def get_device_catalog_themes(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    USER_QUERY[user_id]['device'] = callback_query.data.split('_')[-1]
    
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                            reply_markup=choice_category_db_get_ikb())


async def get_category_catalog_themes(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    device = USER_QUERY[user_id]['device']
    category = callback_query.data.split('_')[-1]
    
    catalog = await get_themes_from_catalog(device, category)
    USER_THEME_CATALOG[user_id] = {}
    USER_THEME_CATALOG[user_id]['catalog'] = catalog
    USER_THEME_CATALOG[user_id]['start'] = 5
    USER_THEME_CATALOG[user_id]['end'] = 11
    
    if catalog:
        await callback_query.message.answer(text=messages.MESSAGE_OUR_THEMES,
                                reply_markup=nex_themes_keyboard())
        for theme in catalog[:5]:
            await callback_query.message.answer_photo(photo=theme['preview'])
            await callback_query.message.answer_document(document=theme['theme'])
    else:
        await callback_query.message.answer(text=messages.MESSAGE_NO_THEMES_IN_CATALOG)


async def get_next_themes(message: Message, bot: Bot):
    user_id = message.from_user.id
    if await is_user_subscribed(message, bot) and is_private_chat(message):
        catalog = USER_THEME_CATALOG[user_id]['catalog']
        start = USER_THEME_CATALOG[user_id]['start']
        end = USER_THEME_CATALOG[user_id]['end']
        
        if catalog[start:end]: 
            for theme in catalog[start:end]:
                await message.answer_photo(photo=theme['preview'])
                await message.answer_document(document=theme['theme'])
            
            USER_THEME_CATALOG[user_id]['start'] += start
            USER_THEME_CATALOG[user_id]['end'] += end
        else:
            await message.delete()
            await message.answer(text=messages.MESSAGE_NO_MORE_THEMES)
        


async def go_to_main_menu(message: Message, bot: Bot):
    user_id = message.from_user.id
    USER_QUERY[user_id] = {}
    USER_THEME_CATALOG[user_id] = {}
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_BACK,
                            reply_markup=user_keyboard(user_id))
