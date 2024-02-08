import os

from aiogram.types import CallbackQuery, FSInputFile

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.user import User


async def all_users_to_txt(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    
    users_id = await session.scalars(select(User.id).where(User.chat_type=='private'))
    users_id = list(users_id)
    file_path = os.path.join('statistica', 'src', 'users.txt')

    with open(file_path, "w") as file:
        for user_id in users_id:
            file.write(str(user_id) + "\n")
    
    await callback_query.message.answer_document(document=FSInputFile(path=file_path))




async def all_active_users_to_txt(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.message.delete()
    
    users_id = await session.scalars(select(User.id).where(and_(User.chat_type=='private',
                                                          User.active==True)))
    users_id = list(users_id)
    file_path = os.path.join('statistica', 'src', 'active_users.txt')

    with open(file_path, "w") as file:
        for user_id in users_id:
            file.write(str(user_id) + "\n")

    await callback_query.message.answer_document(document=FSInputFile(path=file_path))
