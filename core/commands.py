from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllChatAdministrators

from config.messages import START_COMMAND_DESCRIPTION


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description=START_COMMAND_DESCRIPTION
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands, BotCommandScopeAllChatAdministrators())
