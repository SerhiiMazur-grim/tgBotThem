from datetime import datetime
import logging

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from config import messages
from core import inline_keybords, reply_keybords
from database.models.user import User


async def get_full_statistica(message: Message, session: AsyncSession):
    await message.delete()
    
    users = await session.scalars(select(User))
    total_users = len(list(users))
    
    refer_users = None
    active_users = None
    not_active_users = None
    total_priv_chats = None
    active_priv_chats = None
    total_group_chats = None
    active_group_chats = None
    
    await message.answer_photo(photo='AgACAgIAAxkBAAIK1mV8QsjPPraAQ84AAeXm60eD5VhfnQAC1NIxG4mb4EtoJSNVJfQRiAEAAwIAA3gAAzME',
                               caption=messages.full_statistica_caption(
                                   total_users=total_users,
                                   refer_users=refer_users,
                                   active_users=active_users,
                                   not_active_users=not_active_users,
                                   total_priv_chats=total_priv_chats,
                                   active_priv_chats=active_priv_chats,
                                   total_group_chats=total_group_chats,
                                   active_group_chats=active_group_chats,
                               ))
    
    
