from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy import update
from sqlalchemy.future import select

from database.models.user import User


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

            if event.chat_join_request:
                return

            if event_chat:
                user = await session.scalar(
                    select(User).where(User.id == event_chat.id)
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
                        id=event_chat.id,
                        chat_type=event_chat.type,
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
                data["chat_type"] = event_chat.type
            data["session"] = session
            
            return await handler(event, data)
