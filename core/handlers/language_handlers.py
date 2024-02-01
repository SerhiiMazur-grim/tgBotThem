from datetime import datetime
import logging

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from config import messages
from core import inline_keybords, reply_keybords
from core.states import AddLanguageState, GetLanguageCatalogState, AddLanguageCat, LanguagesCatalogState
from database.models.language_catalog import LanguageInCatalog
from database.models.language_category import LanguageCategory


USER_LANGUAGE_CATALOG = {}
logger = logging.getLogger(__name__)


async def admin_language_catalog(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ADMIN_LANGUAGE_CATALOG,
                         reply_markup=reply_keybords.admin_language_catalog_kb()
                         )


async def admin_language_category(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_ADMIN_CATEGORY_MENU,
                         reply_markup=inline_keybords.admin_add_language_category_ikb()
                         )


async def admin_start_add_language_category(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(AddLanguageCat.category)
    await callback_query.message.answer(text=messages.MESSAGE_ADMIN_INPUT_LANGUAGE_CATEGORY)


async def admin_get_language_category(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text
    if text:
        try:
            theme_category = LanguageCategory(
                title=text,
                create_date=datetime.utcnow()
            )
            session.add(theme_category)
            await session.commit()
            await state.clear()
            await message.reply(text=messages.MESSAGE_ADMIN_INPUT_LANGUAGE_CATEGORY_DONE)
        except:
            await message.reply(text=messages.MESSAGE_ADMIN_ADD_LANGUAGE_CATEGORY_ERR)
    else:
        await message.reply(text=messages.MESSAGE_ADMIN_INPUT_LANGUAGE_CATEGORY_ERR)


async def admin_start_delete_language_category(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    
    categories = await session.scalars(select(LanguageCategory))
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_THEME_CAT_TO_DELETE,
                                        reply_markup=inline_keybords.admin_del_language_category_ikb(categories)
                                        )


async def admin_delete_language_category(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    cat_id = callback_query.data.split('_')[-1]
    
    try:
        cat = await session.scalar(select(LanguageCategory).where(LanguageCategory.id==int(cat_id)))
        await session.delete(cat)
        await session.commit()
        await callback_query.message.answer(text=messages.MESSAGE_LANGUAGE_CAT_IS_DELETE)
    
    except Exception as e:
        await callback_query.message.answer(text=messages.MESSAGE_LANGUAGE_CAT_DELETE_ERR)
        logger.error(e)

#-----------------------------------------------------------------------

async def start_add_language(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(AddLanguageState.device)
    await message.answer_poll(
        question=messages.MESSAGE_CHOICE_DEVICE_FOR_LANGUAGE,
        options=messages.DEVICE_FOR_LANGUAGE,
        is_anonymous=False,
        allows_multiple_answers=True
    )


async def add_language_device(poll: PollAnswer, bot: Bot, state: FSMContext, session: AsyncSession):
    devices = [messages.DEVICE_FOR_LANGUAGE[i] for i in poll.option_ids]
    device = {
        'android': True if 'android' in devices else False,
        'ios': True if 'ios' in devices else False,
        'computer': True if 'computer' in devices else False,
    }
    await state.update_data(device=device)
    await state.set_state(AddLanguageState.category)
    categories = await session.scalars(select(LanguageCategory))
    cat_list = list(categories)
    if cat_list:
        await bot.send_message(chat_id=poll.user.id,
                                text=messages.MESSAGE_CHOICE_CATEGORY_FOR_LANGUAGE,
                                reply_markup=inline_keybords.choice_category_lang_ikb(cat_list))
    else:
        await state.clear()
        await bot.send_message(chat_id=poll.user.id, text=messages.MESSAGE_NO_CATEGORIES)


async def add_language_category(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    category = callback_query.data.split('_')[-1]
    await state.update_data(category=category)
    await state.set_state(AddLanguageState.preview)
    await callback_query.message.answer(text=messages.MESAGE_SEND_ME_PREVIEW_AND_TEXT, parse_mode=ParseMode.HTML)


async def add_previev_and_desc_for_language(message: Message, state: FSMContext, session: AsyncSession):
    preview = message.photo[-1].file_id
    caption = message.caption
    data = await state.get_data()
    preview_list = data.get('preview')
    
    if data.get('caption') is None:
        await state.update_data(caption=caption)
    
    if preview_list is None:
        await state.update_data(preview=[preview])
    else:
        preview_list.append(preview)
        if len(preview_list) == 3:
            try:
                language = LanguageInCatalog(
                    preview=', '.join(preview_list),
                    text=data['caption'],
                    android=data['device']['android'],
                    computer=data['device']['computer'],
                    ios=data['device']['ios'],
                    category_id=int(data['category']),
                    join_date=datetime.utcnow()
                )
                session.add(language)
                
                await session.commit()
                await state.clear()
                await message.answer(text=messages.MESSAGE_LANGUAGE_IS_SAVE)
                
            except Exception as e:
                await message.answer(text=messages.MESSAGE_ADD_LANGUAGE_TO_CATALOG_ERR)
                logger.error(e)
        else: 
            await state.update_data(preview=preview_list)
        

async def get_catalog_languages(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(GetLanguageCatalogState.device)
    await message.delete()
    await message.answer(text=messages.BUTTON_LANGUAGE_CATALOG,
                         reply_markup=reply_keybords.catalog_language_keyboard())
    await message.answer(text=messages.MESSAGE_CHOICE_DEVICE_FOR_LANG,
                            reply_markup=inline_keybords.choice_device_lang_get_ikb())


async def get_device_catalog_languages(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    device = callback_query.data.split('_')[-1]
    await state.update_data(device=device)
    await state.set_state(GetLanguageCatalogState.category)
    
    categories = await session.scalars(select(LanguageCategory))
    cat_list = list(categories)
    if cat_list:
        await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                                reply_markup=inline_keybords.choice_category_lang_db_get_ikb(cat_list))
    else:
        await state.clear()
        await callback_query.message.answer(text=messages.MESSAGE_NO_CATEGORIES)
    

async def get_category_catalog_themes(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.answer()
    data = await state.get_data()
    device = data['device']
    category = callback_query.data.split('_')[-1]
    await state.clear()

    if device=='android':
        catalog = await session.scalars(select(LanguageInCatalog).where(
            and_(
                LanguageInCatalog.category_id==int(category),
                LanguageInCatalog.android==True
            )
        ))
    elif device=='computer':
        catalog = await session.scalars(select(LanguageInCatalog).where(
            and_(
                LanguageInCatalog.category_id==int(category),
                LanguageInCatalog.computer==True
            )
        ))
    else:
        catalog = await session.scalars(select(LanguageInCatalog).where(
            and_(
                LanguageInCatalog.category_id==int(category),
                LanguageInCatalog.ios==True
            )
        ))
    catalog = list(catalog)
    await state.set_state(LanguagesCatalogState)
    await state.set_data({
        'catalog': catalog,
        'start': 2,
        'end': 5,
    })
    
    if catalog:
        await callback_query.message.answer(text=messages.MESSAGE_OUR_LANGUAGES,
                                reply_markup=reply_keybords.nex_languages_keyboard())
        for language in catalog[:2]:
            send_data = []
            for prewiew in language.preview.split(', '):
                if not send_data:
                    caption = language.text
                else: caption = None
                send_data.append(InputMediaPhoto(
                    media=prewiew,
                    caption=caption
                ))
            await callback_query.message.answer_media_group(media=send_data)
    else:
        await callback_query.message.answer(text=messages.MESSAGE_NO_LANGUAGES_IN_CATALOG)


async def get_next_languages(message: Message, state: FSMContext):
    data = await state.get_data()
    catalog = data['catalog']
    start = data['start']
    end = data['end']
    
    if catalog[start:end]: 
        for language in catalog[start:end]:
            send_data = []
            for prewiew in language.preview.split(', '):
                if not send_data:
                    caption = language.text
                else: caption = None
                send_data.append(InputMediaPhoto(
                    media=prewiew,
                    caption=caption
                ))
            await message.answer_media_group(media=send_data)
        
        await state.update_data(start=start+start)
        await state.update_data(end=end+end)
    else:
        await message.delete()
        await message.answer(text=messages.MESSAGE_NO_MORE_LANGUAGES)


async def go_to_main_menu_from_lang_catalog(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.delete()
    await message.answer(text=messages.BUTTON_BACK_FROM_LANG_CAT,
                            reply_markup=reply_keybords.user_keyboard(user_id))
