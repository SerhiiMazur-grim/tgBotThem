from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, and_

from config import messages
from database.models.user import User
from database.models.referals import Referal


async def detail_referal_statistica(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    
    ref = callback_query.data.split('_')[-1]
    
    referal = await session.scalar(select(Referal).where(Referal.ref==ref))
    blocked_ref = await session.scalars(select(User.id).where(and_(
        User.ref==ref,
        User.active==False
    )))
    sub_ref = await session.scalars(select(User.id).where(and_(
        User.ref==ref,
        User.sub==True
    )))
    
    ref_id = referal.id
    ref_url = referal.ref
    ref_join_date = referal.join_date
    ref_total_users = referal.total_users
    ref_active_users = referal.active_users
    ref_block_users = len(list(blocked_ref))
    ref_sub_users = len(list(sub_ref))
    
    await callback_query.message.answer(text=messages.referal_detail(
        ref_id=ref_id,
        ref_url=ref_url,
        ref_join_date=ref_join_date,
        ref_total_users=ref_total_users,
        ref_active_users=ref_active_users,
        ref_block_users=ref_block_users,
        ref_sub_users=ref_sub_users
        
    ))
