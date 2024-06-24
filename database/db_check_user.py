from datetime import datetime

from aiogram.types import Message
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User
from database.models.referals import Referal


async def get_or_create_user(message: Message, session: AsyncSession):
    chat_id = message.chat.id
    chat_type = message.chat.type
    user = await session.scalar(
        select(User).where(User.id == chat_id)
    )
    
    premium = False
    if chat_type == 'private':
        user_premium = message.from_user.is_premium
        premium = user_premium if user_premium != None else False

    if not user:
        ref = None
        
        split_text = message.text.split() if message.text else ""
        
        if (
            len(split_text) > 1 
            and split_text[0] == "/start"
            and not split_text[1].startswith("val_")
        ):
            ref = split_text[1]
            referal = await session.scalar(
                select(Referal).where(Referal.ref == ref)
            )
            if not referal:
                referal = Referal(
                    ref=ref,
                    total_users=1,
                    active_users=1,
                    join_date=datetime.utcnow()
                )
                session.add(referal)
                await session.commit()
                
            else:
                await session.execute(
                    update(Referal)
                    .where(Referal.ref==ref)
                    .values(total_users = referal.total_users+1,
                            active_users = referal.active_users+1)
                )
                await session.commit()

        user = User(
            id=chat_id,
            chat_type=chat_type,
            join_date=datetime.utcnow(),
            last_active=datetime.utcnow(),
            premium=premium,
            ref=ref,
        )
        session.add(user)
    else:
        await session.execute(
                        update(User)
                        .where(User.id == user.id)
                        .values(last_active=datetime.utcnow(),
                                active=True,
                                premium=premium)
                    )
    
    await session.commit()
