import logging
from datetime import datetime

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from config import messages
from config.api_keys import ADMINS
from core.commands import set_chat_commands
from core.utils import is_user_subscribed
from core.keyboards.inline_keybords import add_bot_to_chat_inl_keyboard, go_to_bot_ikb, choose_op_to_del
from core.keyboards.reply_keybords import user_keyboard, admin_keyboard
from core.states import OPKanal, OPDelKanal
from database import get_or_create_user
from database.models.chanel_op import ChanelOP
import core.middleware as md 


logger = logging.getLogger(__name__)


async def command_set_op(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(OPKanal.chanel_id)
    await message.answer(text="Скиньте id каналу у форматі: '@pruklad_id_kanala'")


async def set_op_url(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text:
        return
    if text[0]!='@':
        text = '@'+text
    await state.update_data(chanel_id=text)
    await state.set_state(OPKanal.invate_url)
    await message.answer('Скиньте реферальну силку')
    
    
async def get_op_url(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text.strip()
    if not text:
        return
    data = await state.get_data()
    chanel_id = data.get('chanel_id')
    
    try:
        op = ChanelOP(
            chanel_id = chanel_id,
            invate_url = text
        )
        session.add(op)
        op_model = await session.commit()
        md.op_ids = []
        
    except Exception as e:
                await message.answer(text='Сталася помилка')
                logger.error(e)
                
    await state.clear()
    await message.answer('ОП додано')


async def del_op(message: Message, state: FSMContext, op_list):
    await message.delete()
    # op_list = data.get('op_list')
    if not op_list:
        return message.answer('Список ОП пустий')
    
    op_id = [k.get('chanel_id') for k in op_list]
    await state.set_state(OPDelKanal.chanel_id)
    await message.answer(text='Оберіть канал для видалення з ОП:',
                         reply_markup=choose_op_to_del(op_id))


async def op_is_del(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()
    chanel_id = call.data
    if chanel_id == 'abort':
        await state.clear()
        return
    
    await state.clear()
    try:
        await session.execute(delete(ChanelOP).where(ChanelOP.chanel_id == chanel_id))
        await session.commit()
        md.op_ids = []
        await call.message.answer(text=f'Канал {chanel_id} видалено з ОП')
    except Exception as e:
                await call.message.answer(text='Сталася помилка')
                logger.error(e)
