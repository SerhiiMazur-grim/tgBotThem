from aiogram.types import Message
from aiogram.filters import BaseFilter

from config.api_keys import ADMINS


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        
        user_id = message.from_user.id
        
        return str(user_id) in ADMINS


class IsPrivateChatFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        
        chat_type = message.chat.type
        
        return chat_type == 'private'
