import logging

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import messages
from core.keyboards.inline_keybords import fonts_ikb
from core.utils import ch_text_font
from core.states import GetFontTextState


logger = logging.getLogger(__name__)


async def font_catalog(message: Message, state: FSMContext):
    await state.set_state(GetFontTextState.text)
    await message.delete()
    await message.answer(text=messages.MESSAGE_SEND_ME_TEXT)


async def get_text_from_user(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.reply(text=messages.MESSAGE_CHOICE_FONT, reply_markup=fonts_ikb())


async def change_font_in_text(callback_query: CallbackQuery, state: FSMContext):
    try:
        await callback_query.message.delete()
    except Exception as e:
        logger.error(e)

    font = callback_query.data
    data = await state.get_data()
    await state.clear()
        
    if data:
        if type(data) is str:
            new_text = await ch_text_font(data['text'], font)
            await callback_query.message.answer(text=new_text)
