from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy import update
from sqlalchemy.future import select

from database.models.user import User
from database.models.send_post import SendPost
from database.models.referals import Referal


class UserMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        async with self.sessionmaker() as session:
            event_chat = data.get("event_chat")
            event_from_user = data.get("event_from_user")

            if event.chat_join_request:
                return
            
            message = event.message
            if event_chat:
                if event_chat.type != 'private' and message:
                    
                    if message.text:
                        if not message.text.startswith('/start'):
                            return
                    elif message.photo:
                        if message.caption!='/theme':
                            return

            if event_chat:
                user = await session.scalar(
                    select(User).where(User.id == event_chat.id)
                )
                premium = False
                if event_chat.type == 'private':
                    premium = event_from_user.is_premium if event_from_user.is_premium != None else False

                if not user:
                    ref = None
                    
                    if event.message:
                        split_text = event.message.text.split() if event.message.text else ""
                        
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
                        id=event_chat.id,
                        chat_type=event_chat.type,
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
                data["user"] = user
                data["chat_type"] = event_chat.type
            
            post_db = await session.scalar(select(SendPost))
            if not post_db:
                db_instance = SendPost()
                session.add(db_instance)
                await session.commit()
                post_db = await session.scalar(select(SendPost))
                
            data['post_data'] = post_db
            
            data["session"] = session
            
            return await handler(event, data)
