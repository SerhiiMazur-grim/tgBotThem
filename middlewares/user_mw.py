from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy import update
from sqlalchemy.future import select

from database.models.user import User
from database.models.group_chat import GroupChat


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
            event_user = data.get("event_from_user")
            event_chat = data.get("event_chat")

            if event.chat_join_request:
                return
            
            if event_chat.type != 'private':
                group_chat = await session.scalar(
                    select(GroupChat).where(GroupChat.id == event_chat.id)
                )
                
                if not group_chat and event.message:
                    if event.message.text.startswith('/start'):
                        group_chat = GroupChat(
                            id=event_chat.id,
                            join_date=datetime.utcnow(),
                            last_active=datetime.utcnow(),
                        )
                        session.add(group_chat)
                else:
                    await session.execute(
                                    update(GroupChat)
                                    .where(GroupChat.id == group_chat.id)
                                    .values(last_active=datetime.utcnow())
                                )
                await session.commit()
                data["user"] = group_chat
                data["session"] = session
                
                return await handler(event, data)
                

            if event_user:
                user = await session.scalar(
                    select(User).where(User.id == event_user.id)
                )

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

                    user = User(
                        id=event_user.id,
                        join_date=datetime.utcnow(),
                        last_active=datetime.utcnow(),
                        ref=ref,
                    )
                    session.add(user)
                
                else:
                    await session.execute(
                                    update(User)
                                    .where(User.id == user.id)
                                    .values(last_active=datetime.utcnow())
                                )
                
                await session.commit()
                data["user"] = user
            data["session"] = session
            
            return await handler(event, data)
