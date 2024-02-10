from datetime import datetime
import logging

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import AiogramError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from config import messages
from config.api_keys import ADMINS
from core import inline_keybords, reply_keybords
from core.keyboards.reply_keybords import nex_themes_keyboard, user_keyboard, admin_theme_catalog_kb
from core.keyboards.inline_keybords import admin_add_theme_category_ikb, admin_del_theme_category_ikb
from core.states import AddThemeState, GetThemesCatalogState, AddThemeCat, ThemesCatalogState

from database.models.theme_category import ThemeCategory, ThemeInCatalog


logger = logging.getLogger(__name__)


async def admin_theme_catalog(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ADMIN_THEME_CATALOG,
                         reply_markup=admin_theme_catalog_kb()
                         )


async def admin_theme_category(message: Message, session: AsyncSession):
    categories = await session.scalars(select(ThemeCategory.title))
    cat_list = '\n'.join(list(categories))
    
    await message.delete()
    if cat_list:
        await message.answer(text=f'Список категорий тем:\n{cat_list}',
                            reply_markup=admin_add_theme_category_ikb()
                            )
    else:
        await message.answer(text='Список категорий тем:\nПусто...Пока что категорий нет, создайте категорию.',
                            reply_markup=admin_add_theme_category_ikb()
                            )


async def admin_start_add_theme_category(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(AddThemeCat.category)
    await callback_query.message.answer(text=messages.MESSAGE_ADMIN_INPUT_THEME_CATEGORY)


async def admin_get_theme_category(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text
    if text:
        try:
            theme_category = ThemeCategory(
                title=text,
                create_date=datetime.utcnow()
            )
            session.add(theme_category)
            await session.commit()
            await state.clear()
            await message.reply(text=messages.MESSAGE_ADMIN_INPUT_THEME_CATEGORY_DONE)
        except:
            await message.reply(text=messages.MESSAGE_ADMIN_ADD_THEME_CATEGORY_ERR)
    else:
        await message.reply(text=messages.MESSAGE_ADMIN_INPUT_THEME_CATEGORY_ERR)


async def admin_start_delete_theme_category(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    
    categories = await session.scalars(select(ThemeCategory))
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_THEME_CAT_TO_DELETE,
                                        reply_markup=admin_del_theme_category_ikb(categories)
                                        )


async def admin_delete_theme_category(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    cat_id = callback_query.data.split('_')[-1]
    
    try:
        cat = await session.scalar(select(ThemeCategory).where(ThemeCategory.id==int(cat_id)))
        await session.delete(cat)
        await session.commit()
        await callback_query.message.answer(text=messages.MESSAGE_THEME_CAT_IS_DELETE)
    
    except Exception as e:
        await callback_query.message.answer(text=messages.MESSAGE_THEME_CAT_DELETE_ERR)
        logger.error(e)


#-----------------------------------------------------------------------------------


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
    await callback_query.message.delete()
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


async def add_theme_file(message: Message, state: FSMContext, session: AsyncSession):
    file = message.document
    if file.file_name.split('.')[-1] in ('attheme', 'tdesktop-theme', 'tgios-theme'):
        await state.update_data(file=file.file_id)
        await state.set_state(AddThemeState.category)
        categories = await session.scalars(select(ThemeCategory))
        cat_list = list(categories)
        if cat_list:
            await message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                                        reply_markup=inline_keybords.choice_category_ikb_keyboard(cat_list))
        else:
            await state.clear()
            await message.answer(text=messages.MESSAGE_NO_CATEGORIES)
    else:
        await message.answer(text=messages.MESSAGE_IS_NOT_THEME)
      

async def add_theme_category(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.message.delete()
    category_id = callback_query.data.split('_')[-1]
    theme_data = await state.update_data(category=category_id)
    await state.clear()
    
    preview = theme_data['preview']
    theme = theme_data['file']
    device = theme_data['device']
    
    try:
        theme_to_catalog = ThemeInCatalog(
            preview=preview,
            file=theme,
            device=device,
            category_id=int(category_id),
            join_date=datetime.utcnow()
        )
        session.add(theme_to_catalog)
        await session.commit()
        await callback_query.message.answer(text=messages.MESSAGE_ADDED_TO_DB)
        
    except Exception as e:
        await callback_query.message.answer(text=messages.MESSAGE_ADD_THEME_TO_CATALOG_ERR)
        logger.error(e)
    

#-------------------------------------------------------------------------------


async def get_catalog_themes(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(GetThemesCatalogState.device)
    await message.answer(text=messages.BUTTON_THEME_CATALOG,
                         reply_markup=reply_keybords.catalog_theme_keyboard())
    await message.answer(text=messages.MESSAGE_CHOICE_DEVICE,
                            reply_markup=inline_keybords.choice_device_db_get_ikb())


async def get_device_catalog_themes(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    try:
        await callback_query.message.delete()
    except Exception as e:
        logger.error(e)
        return
    
    device = callback_query.data.split('_')[-1]
    await state.update_data(device=device)
    await state.set_state(GetThemesCatalogState.category)
    categories = await session.scalars(select(ThemeCategory))
    cat_list = list(categories)
    if cat_list:
        await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                                reply_markup=inline_keybords.choice_category_db_get_ikb(cat_list))
    else:
        await state.clear()
        await callback_query.message.answer(text=messages.MESSAGE_NO_CATEGORIES)


async def get_category_catalog_themes(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    try:
        await callback_query.message.delete()
    except Exception as e:
        logger.error(e)
        return
    
    user_id = callback_query.from_user.id
    category = callback_query.data.split('_')[-1]
    try:
        category = int(category)
    except Exception as e:
        logger.error(e)
        return
    
    data = await state.get_data()
    await state.clear()
    
    catalog = await session.scalars(select(ThemeInCatalog).where(
        and_(
            ThemeInCatalog.category_id==category,
            ThemeInCatalog.device==data['device']
        )
    ))
    catalog = list(catalog)
    
    await state.set_state(ThemesCatalogState)
    await state.set_data({
        'catalog': catalog,
        'start': 5,
        'end': 11,
    })
    
    if catalog:
        await callback_query.message.answer(text=messages.MESSAGE_OUR_THEMES,
                                reply_markup=nex_themes_keyboard())
        for theme in catalog[:5]:
            theme_id = theme.id
            try:    
                await callback_query.message.answer_photo(photo=theme.preview)
                await callback_query.message.answer_document(document=theme.file, caption=messages.CAPTION_TO_THEME_IN_CATALOG)
                if str(user_id) in ADMINS:
                    await callback_query.message.answer(text=messages.MESSAGE_DELETE_THEME,
                                                    reply_markup=inline_keybords.delete_theme_ikb(theme_id))
                    
            except AiogramError as er:
                logger.error(er)
    else:
        await callback_query.message.answer(text=messages.MESSAGE_NO_THEMES_IN_CATALOG)


async def get_next_themes(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    catalog = data.get('catalog')
    
    if catalog:
        start = data['start']
        end = data['end']
        
        if catalog[start:end]: 
            for theme in catalog[start:end]:
                theme_id = theme.id
                try:
                    await message.answer_photo(photo=theme.preview)
                    await message.answer_document(document=theme.file, caption=messages.CAPTION_TO_THEME_IN_CATALOG)
                    if str(user_id) in ADMINS:
                        await message.answer(text=messages.MESSAGE_DELETE_THEME,
                                                        reply_markup=inline_keybords.delete_theme_ikb(theme_id))
                except AiogramError as er:
                    logger.error(er)
                    
            await state.update_data(start=start+start)
            await state.update_data(end=end+end)
        else:
            await message.delete()
            await message.answer(text=messages.MESSAGE_NO_MORE_THEMES)
        

async def admin_delete_theme(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    theme_id = callback_query.data.split('_')[-1]
    try:
        language = await session.scalar(select(ThemeInCatalog).where(ThemeInCatalog.id==int(theme_id)))
        await session.delete(language)
        await session.commit()
        await callback_query.message.answer(text=messages.MESSAGE_THEME_IS_DELETE)
    
    except Exception as e:
        await callback_query.message.answer(text=messages.MESSAGE_THEME_IS_DELETE_ERR)
        logger.error(e)


async def go_to_main_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.delete()
    await message.answer(text=messages.MESSAGE_ON_BACK,
                            reply_markup=user_keyboard(user_id))
