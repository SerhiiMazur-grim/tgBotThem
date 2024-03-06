import random

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config import messages
from core.keyboards import inline_keybords
from database.models.theme_catalog import ThemeInCatalog
from database.models.language_catalog import LanguageInCatalog
from core.states import RandomThemeState, RandomLanguageState


DEVICE_DICT = {
    'android': messages.ANDROID,
    'iphone': messages.IPHONE,
    'desktop': messages.FOR_PC
}


async def random_theme_command(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name
    await state.set_state(RandomThemeState.device)
    await message.answer(text=messages.message_what_your_device(user_full_name),
                         reply_markup=inline_keybords.choose_device_for_random_theme_kb())


async def send_random_theme(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.message.delete()
    await state.clear()

    device = callback_query.data.split('_')[-1]

    if device in ('android', 'iphone', 'desktop'):
        themes = (await session.scalars(select(ThemeInCatalog).where(ThemeInCatalog.device == device))).all()
        
        if themes:
            theme: ThemeInCatalog = random.choice(themes)
        else:
            return callback_query.message.answer(text=messages.MESSAGE_NO_THEMES_IN_CATALOG)
        
        await callback_query.message.answer_photo(photo=theme.preview,
                                                  caption=messages.preview_caption_on_theme(DEVICE_DICT.get(device)),
                                                  reply_markup=inline_keybords.send_random_theme(theme.id))
    else:
        return callback_query.message.answer(text=messages.MESSAGE_ON_RANDOM_SOME_ERROR)


async def send_theme_file_to_group(callback_query: CallbackQuery, session: AsyncSession) -> None:
    await callback_query.message.delete()
    theme_id = callback_query.data.split('_')[-1]
    file_id = await session.scalar(select(ThemeInCatalog.file).where(ThemeInCatalog.id==int(theme_id)))
    await callback_query.message.answer_document(document=file_id,
                                                 caption=messages.CAPTION_ON_THEME_FILE)


async def get_random_err(callback_query: CallbackQuery):
    await callback_query.answer(text=messages.MESSAGE_IS_NOT_YOUR_GET_RANDOM,
                                show_alert=True)


async def random_language_command(message: Message, state: FSMContext):
    user_full_name = message.from_user.full_name
    await state.set_state(RandomLanguageState.device)
    await message.answer(text=messages.message_what_your_device(user_full_name),
                         reply_markup=inline_keybords.choose_device_for_random_language_kb())


async def send_random_language(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback_query.message.delete()
    await state.clear()

    device = callback_query.data.split('_')[-1]
        
    send_data = []
    
    if device == 'android':
        languages = (await session.scalars(select(LanguageInCatalog).where(LanguageInCatalog.android==True))).all()
    elif device == 'iphone':
        languages = (await session.scalars(select(LanguageInCatalog).where(LanguageInCatalog.ios==True))).all()
    elif device == 'desktop':
        languages = (await session.scalars(select(LanguageInCatalog).where(LanguageInCatalog.computer==True))).all()
    else:
        return callback_query.message.answer(text=messages.MESSAGE_ON_RANDOM_SOME_ERROR)
    
    if languages:
        language: LanguageInCatalog = random.choice(languages)
    else:
        return callback_query.message.answer(text=messages.MESSAGE_NO_LANGUAGES_IN_CATALOG)
    
    for prewiew in language.preview.split(', '):
        if not send_data:
            caption = language.text
        else: caption = None
        send_data.append(InputMediaPhoto(
            media=prewiew,
            caption=caption,
            parse_mode=ParseMode.HTML
        ))
    await callback_query.message.answer_media_group(media=send_data)
