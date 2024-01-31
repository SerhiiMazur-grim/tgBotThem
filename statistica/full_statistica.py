from datetime import datetime, timedelta

from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from config import messages
from database.models.user import User
from database.models.referals import Referal


async def check_not_active_users(session: AsyncSession):
    current_time = datetime.utcnow()
    inactive_period = current_time - timedelta(days=60)
    
    inactive_users = await session.scalars(select(User).where(User.last_active <= inactive_period))
    
    if inactive_users:
        for user in inactive_users:
            await session.execute(
                update(User)
                .where(User.id == user.id)
                .values(active=False))
            
            if user.ref:
                referal = await session.scalar(select(Referal).where(Referal.ref==user.ref))
                
                await session.execute(
                    update(Referal)
                    .where(Referal.id==referal.id)
                    .values(active_users=referal.active_users-1)
                )
                
        await session.commit()
    
    return 


async def get_full_statistica(message: Message, session: AsyncSession):
    await message.delete()
    
    await check_not_active_users(session)
    
    users = await session.scalars(select(User))
    
    total_users = 0
    refer_users = 0
    total_active_users = 0
    total_priv_chats = 0
    active_priv_chats = 0
    total_group_chats = 0
    active_group_chats = 0
    
    for user in users:
        total_users += 1
        if user.ref:
            refer_users += 1
        if user.active:
            total_active_users += 1
        if user.chat_type=='private':
            total_priv_chats += 1
        if user.chat_type=='private' and user.active:
            active_priv_chats += 1
        if user.chat_type!='private':
            total_group_chats += 1
        if user.chat_type!='private' and user.active:
            active_group_chats += 1
    
    not_active_users = total_users - total_active_users
    not_active_priv_chats = total_priv_chats - active_priv_chats
    not_active_group_chats = total_group_chats - active_group_chats
    
    await message.answer(text=messages.full_statistica_caption(
                                   total_users=total_users,
                                   refer_users=refer_users,
                                   total_active_users=total_active_users,
                                   not_active_users=not_active_users,
                                   total_priv_chats=total_priv_chats,
                                   active_priv_chats=active_priv_chats,
                                   not_active_priv_chats=not_active_priv_chats,
                                   total_group_chats=total_group_chats,
                                   active_group_chats=active_group_chats,
                                   not_active_group_chats=not_active_group_chats
                               ))


