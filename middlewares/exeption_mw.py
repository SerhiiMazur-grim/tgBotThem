from typing import Any, Awaitable, Callable, Dict
import logging
import asyncio
import subprocess

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, Message
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from sqlalchemy.exc import TimeoutError


logger = logging.getLogger(__name__)


class ForbiddenErrorMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        
        bot: Bot = data.get("bot")
        
        try:
            return await handler(event, data)
        
        except TelegramForbiddenError as e:
            user_id = event.from_user.id if isinstance(event, Message) else "unknown"
            logger.error(f"TelegramForbiddenError for chat {user_id}: {e}")
            return
        
        except TelegramRetryAfter as e:
            user_id = event.from_user.id if isinstance(event, Message) else "unknown"
            logger.error(f"TelegramRetryAfter for chat {user_id}: {e}")
            
            if isinstance(event, Message):
                await bot.send_message(event.message.chat.id, f"⛔️Флуд контроль, подождите {e.retry_after} секунд⛔️")
                await asyncio.sleep(e.retry_after)
                return await handler(event, data)
            return
        
        except TimeoutError as e:
            logger.error(f"TimeoutError error in sqlalchemy: {e}")
            command = "sudo systemctl restart theme_bot"
            subprocess.run(command, shell=True)
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return
