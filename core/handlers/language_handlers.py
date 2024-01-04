from aiogram import Bot
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from config import messages
from core.keyboards.reply_keybords import nex_languages_keyboard, user_keyboard
from core.keyboards import inline_keybords
from core.database import get_languages_from_catalog, add_language_to_catalog
from core.states import AddLanguageState, GetLanguageCatalogState


USER_LANGUAGE_CATALOG = {}


async def start_add_language(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(AddLanguageState.device)
    await message.answer_poll(
        question=messages.MESSAGE_CHOICE_DEVICE_FOR_LANGUAGE,
        options=messages.DEVICE_FOR_LANGUAGE,
        is_anonymous=False,
        allows_multiple_answers=True
    )


async def add_language_device(poll: PollAnswer, bot: Bot, state: FSMContext):
    devices = [messages.DEVICE_FOR_LANGUAGE[i] for i in poll.option_ids]
    device = {
        'android': 'True' if 'android' in devices else 'False',
        'ios': 'True' if 'ios' in devices else 'False',
        'computer': 'True' if 'computer' in devices else 'False',
    }
    await state.update_data(device=device)
    await state.set_state(AddLanguageState.category)
    await bot.send_message(chat_id=poll.user.id,
                            text=messages.MESSAGE_CHOICE_CATEGORY_FOR_LANGUAGE,
                            reply_markup=inline_keybords.language_categories_ikb())


async def add_language_category(callback_query: CallbackQuery, state: FSMContext):
    category = callback_query.data.split('_')[-1]
    await state.update_data(category=category)
    await state.set_state(AddLanguageState.preview)
    await callback_query.message.answer(text=messages.MESAGE_SEND_ME_PREVIEW_AND_TEXT, parse_mode=ParseMode.HTML)


async def add_previev_and_desc_for_language(message: Message, state: FSMContext):
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
            await add_language_to_catalog(
                android=data['device']['android'],
                ios=data['device']['ios'],
                computer=data['device']['computer'],
                category=data['category'],
                preview=', '.join(preview_list),
                description=data['caption']
            )
            await state.clear()
            await message.answer(text=messages.MESSAGE_LANGUAGE_IS_SAVE)
        else: 
            await state.update_data(preview=preview_list)
        

async def get_catalog_languages(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(GetLanguageCatalogState.device)
    USER_LANGUAGE_CATALOG[user_id] = {}
    await message.delete()
    await message.answer(text=messages.MESSAGE_CHOICE_DEVICE_FOR_LANG,
                            reply_markup=inline_keybords.choice_device_lang_get_ikb())


async def get_device_catalog_languages(callback_query: CallbackQuery, state: FSMContext):
    device = callback_query.data.split('_')[-1]
    await state.update_data(device=device)
    await state.set_state(GetLanguageCatalogState.category)
    
    await callback_query.message.answer(text=messages.MESSAGE_CHOICE_CATEGORY,
                            reply_markup=inline_keybords.choice_category_lang_db_get_ikb())
    

async def get_category_catalog_themes(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    data = await state.get_data()
    device = data['device']
    category = callback_query.data.split('_')[-1]
    await state.clear()
    
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


async def get_next_languages(message: Message):
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


async def go_to_main_menu_from_lang_catalog(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    USER_LANGUAGE_CATALOG[user_id] = {}
    await message.delete()
    await message.answer(text=messages.BUTTON_BACK_FROM_LANG_CAT,
                            reply_markup=user_keyboard(user_id))
