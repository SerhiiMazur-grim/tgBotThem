from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, \
    BotCommandScopeAllChatAdministrators, BotCommandScopeAllGroupChats, \
    BotCommandScopeChat

from config import messages


async def set_chat_commands(bot: Bot, chat_id) -> None:
    commands = [
        BotCommand(
            command='start',
            description=messages.START_COMMAND_DESCRIPTION
        ),
        BotCommand(
            command='set_wallpaper',
            description=messages.COMMAND_DESCRIPTION_SET_WALLPAPER
        )
    ]
    await bot.set_my_commands(commands=commands,
                              scope=BotCommandScopeChat(chat_id=chat_id))


async def set_commands(bot: Bot):
    commands_private = [
        BotCommand(
            command='start',
            description=messages.START_COMMAND_DESCRIPTION
        )
    ]
    commands_group = [
        BotCommand(command='randomtheme',
                   description=messages.COMMAND_DESCRIPTION_RANDOM_THEME),
        BotCommand(command='randomlanguage',
                   description=messages.COMMAND_DESCRIPTION_RANDOM_LANGUAGE)
    ]
    commands_group_admins = [
        BotCommand(command='start',
                   description=messages.START_COMMAND_DESCRIPTION),
        BotCommand(command='randomtheme',
                   description=messages.COMMAND_DESCRIPTION_RANDOM_THEME),
        BotCommand(command='randomlanguage',
                   description=messages.COMMAND_DESCRIPTION_RANDOM_LANGUAGE)
    ]

    await bot.set_my_commands(commands_private, BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands_group, BotCommandScopeAllGroupChats())
    await bot.set_my_commands(commands_group_admins, BotCommandScopeAllChatAdministrators())
