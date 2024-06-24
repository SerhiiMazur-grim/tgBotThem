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

        if event.chat_join_request:
            return
        
        event_chat = data.get("event_chat")
        message = event.message
        
        if event_chat:
            if event_chat.type != 'private' and message:
                
                if message.text:
                    if not message.text[:6] in ('/start', '/rando'):
                        return
                elif message.photo:
                    if message.caption!='/bg':
                        return
        
        async with self.sessionmaker() as session:
            
            data["chat_type"] = event_chat.type
            
            post_check = data.get('post_check')
            if post_check:
                current_time = datetime.now()
                time_difference = current_time - post_check
                if time_difference.total_seconds() < 60:
                    return handler(event, data)
            
            post_db = await session.scalar(select(SendPost))
            if not post_db:
                db_instance = SendPost()
                session.add(db_instance)
                await session.commit()
                post_db = await session.scalar(select(SendPost))
                
            data['post_data'] = post_db
            data['post_check'] = datetime.now()
            data["session"] = session
            
            return await handler(event, data)
