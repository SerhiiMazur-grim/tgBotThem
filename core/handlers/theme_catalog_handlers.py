from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import messages
from core.keyboards import inline_keybords, reply_keybords
from core.keyboards.reply_keybords import nex_themes_keyboard, user_keyboard
from core.database import get_themes_from_catalog
from core.states import AddThemeState, GetThemesCatalogState
from core.database import add_theme_to_catalog


USER_THEME_CATALOG = {}


async def start_add_theme(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(AddThemeState.device)
    await message.answer(text=messages.MESSAGE_CHOICE_DEVICE,
                            reply_markup=inline_keybords.choice_device_db_ikb_keyboard())


async def abort_add_theme(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await callback_query.answer(text='Cancelled')
    


async def add_theme_device(callback_query: CallbackQuery, state: FSMContext):
    device = callback_query.data.split('_')[-1]
    await state.update_data(device=device)
    await state.set_state(AddThemeState.preview)
    await callback_query.message.answer(text=messages.MESSAGE_SEND_PREVIEW_THEME,
                                        reply_markup=inline_keybords.abort_add_theme_ikb())


async def add_theme_preview(message: Message, state: FSMContext):
    preview = message.photo[-1].file_id
    await state.update_data(preview=preview)
    await state.set_state(AddThemeState.file)
    await message.answer(text=messages.MESSAGE_SEND_THEME_FILE,
                         reply_markup=inline_keybords.abort_add_theme_ikb())


async def add_theme_file(message: Message, state: FSMContext):
    file = message.document
    if file.file_name.split('.')[-1] in ('attheme', 'tdesktop-theme', 'tgios-theme'):
        await state.update_data(file=file.file_id)
        await state.set_state(AddThemeState.category)
        await message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                                     reply_markup=inline_keybords.choice_category_ikb_keyboard())
    else:
        await message.answer(text=messages.MESSAGE_IS_NOT_THEME)
      

async def add_theme_category(callback_query: CallbackQuery, state: FSMContext):
    category = callback_query.data.split('_')[-1]
    theme_data = await state.update_data(category=category)
    await state.clear()
    
    preview = theme_data['preview']
    theme = theme_data['file']
    device = theme_data['device']
    
    await add_theme_to_catalog(category, preview, theme, device)
    
    await callback_query.message.answer(text=messages.MESSAGE_ADDED_TO_DB)


#-------------------------------------------------------------------------------


async def get_catalog_themes(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(GetThemesCatalogState.device)
    await message.answer(text=messages.BUTTON_THEME_CATALOG,
                         reply_markup=reply_keybords.catalog_theme_keyboard())
    await message.answer(text=messages.MESSAGE_CHOICE_DEVICE,
                            reply_markup=inline_keybords.choice_device_db_get_ikb())


async def get_device_catalog_themes(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    device = callback_query.data.split('_')[-1]
    await state.update_data(device=device)
    await state.set_state(GetThemesCatalogState.category)
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                            reply_markup=inline_keybords.choice_category_db_get_ikb())


async def get_category_catalog_themes(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    category = callback_query.data.split('_')[-1]
    data = await state.get_data()
    await state.clear()
    
    catalog = await get_themes_from_catalog(data['device'], category)
    user_id = callback_query.from_user.id
    USER_THEME_CATALOG[user_id] = {}
    USER_THEME_CATALOG[user_id]['catalog'] = catalog
    USER_THEME_CATALOG[user_id]['start'] = 5
    USER_THEME_CATALOG[user_id]['end'] = 11
    
    if catalog:
        await callback_query.message.answer(text=messages.MESSAGE_OUR_THEMES,
                                reply_markup=nex_themes_keyboard())
        for theme in catalog[:5]:
            await callback_query.message.answer_photo(photo=theme['preview'])
            await callback_query.message.answer_document(document=theme['theme'], caption=messages.CAPTION_TO_THEME_IN_CATALOG)
    else:
        await callback_query.message.answer(text=messages.MESSAGE_NO_THEMES_IN_CATALOG)


async def get_next_themes(message: Message, bot: Bot):
    user_id = message.from_user.id
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
        


async def go_to_main_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        
    USER_THEME_CATALOG[user_id] = {}
    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_BACK,
                            reply_markup=user_keyboard(user_id))
