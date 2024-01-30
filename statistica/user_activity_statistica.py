from datetime import datetime, timedelta

from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from config import messages
from database.models.user import User


async def user_activity_per_day(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    current_time = datetime.utcnow()
    one_day = current_time - timedelta(hours=24)
    
    users = await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type=='private',
        User.last_active>=one_day
    )))
    chats = await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type!='private',
        User.last_active>=one_day
    )))
    users_count = len(list(users))
    chats_count = len(list(chats))
    total_count = users_count+chats_count

    await callback_query.message.answer(text=messages.active_users_per_day_message(
        users_count,
        chats_count,
        total_count
        ))


async def user_activity_per_week(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    current_time = datetime.utcnow()
    one_week = current_time - timedelta(days=7)
    
    users = await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type=='private',
        User.last_active>=one_week
    )))
    chats = await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type!='private',
        User.last_active>=one_week
    )))
    users_count = len(list(users))
    chats_count = len(list(chats))
    total_count = users_count+chats_count

    await callback_query.message.answer(text=messages.active_users_per_week_message(
        users_count,
        chats_count,
        total_count
        ))


async def user_activity_per_month(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    current_time = datetime.utcnow()
    one_month = current_time - timedelta(days=30)
    
    users = await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type=='private',
        User.last_active>=one_month
    )))
    chats = await session.scalars(select(User.id).where(and_(
        User.active==True,
        User.chat_type!='private',
        User.last_active>=one_month
    )))
    users_count = len(list(users))
    chats_count = len(list(chats))
    total_count = users_count+chats_count

    await callback_query.message.answer(text=messages.active_users_per_month_message(
        users_count,
        chats_count,
        total_count
        ))
