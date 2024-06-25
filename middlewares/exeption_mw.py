from typing import Any, Awaitable, Callable, Dict
import logging

from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from aiogram.exceptions import TelegramForbiddenError


logger = logging.getLogger(__name__)


class ForbiddenErrorMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        
        try:
            return await handler(event, data)
        
        except TelegramForbiddenError as e:
            user_id = event.from_user.id if isinstance(event, Message) else "unknown"
            logger.error(f"TelegramForbiddenError for user {user_id}: {e}")
            return
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return