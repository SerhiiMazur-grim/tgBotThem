from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config import messages
from core import inline_keybords, reply_keybords
from database.models.referals import Referal


async def statistic_menu(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_IS_STATISTIC_MENU,
                         reply_markup=reply_keybords.admin_statistic_menu_kb())


async def active_statistic_menu(message: Message):
    await message.delete()
    await message.answer(text=messages.MESSAGE_PERIOD_OF_ACTIVE_CHOICE,
                         reply_markup=inline_keybords.active_statistic_menu_ikb())
    

async def referals_statistic_menu(message: Message, session: AsyncSession):
    await message.delete()
    referals = await session.scalars(select(Referal.ref))
    if referals:    
        await message.answer(text=messages.MESSAGE_CHOICE_REFERAL,
                            reply_markup=inline_keybords.choice_referal_ikb(referals))
    else:
        await message.answer(text=messages.MESSAGE_NO_REFERALS)
