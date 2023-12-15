import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

from config.api_keys import TOKEN_API
from config import messages
from core.handlers.basic import start_bot, command_start, sub_checker, command_create_theme, command_add_to_chat, command_faq
from core.handlers.theme_handlers import handle_photo, handler_abort, handler_device, handler_background_color, \
    handler_primary_text_color, handler_secondary_text_color, handler_alfa_background_color, handler_auto_theme, \
    handler_back_to_device_choose, handler_back_to_background_color_choose, handler_back_to_primary_text_color_choose, \
    handler_back_to_secondary_text_color_choose, start_add_theme, add_theme_category, add_theme_device
from core.middleware import CleanupMiddleware, check_and_delete_files


async def main():
    await check_and_delete_files()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN_API, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()

    dp.message.middleware.register(CleanupMiddleware())
    
    # basic handlers
    dp.startup.register(start_bot)
    dp.message.register(command_start, Command('start'))
    dp.message.register(command_create_theme, F.text == messages.BUTTON_CREATE_THEME)
    dp.message.register(command_add_to_chat, F.text == messages.BUTTON_ADD_TO_CHAT)
    dp.message.register(command_faq, F.text == messages.BUTTON_FAQ)
    dp.callback_query.register(sub_checker, F.data == 'sub_check')


    dp.message.register(start_add_theme, F.text == messages.BUTTON_ADD_THEME)
    dp.message.register(handle_photo, F.photo)
    dp.message.register(handle_photo, F.document)
    dp.callback_query.register(add_theme_category, F.data.startswith('cat_'))
    dp.callback_query.register(handler_abort, F.data == 'abort')
    dp.callback_query.register(handler_device, F.data.startswith('device_'))
    dp.callback_query.register(add_theme_device, F.data.startswith('db-dev_'))
    dp.callback_query.register(handler_background_color, F.data.startswith('background_color_'))
    dp.callback_query.register(handler_primary_text_color, F.data.startswith('primary_text_color_'))
    dp.callback_query.register(handler_secondary_text_color, F.data.startswith('secondary_text_color_'))
    dp.callback_query.register(handler_alfa_background_color, F.data.startswith('background_alfa_'))
    dp.callback_query.register(handler_auto_theme, F.data == 'auto_background_color')

    dp.callback_query.register(handler_back_to_device_choose, F.data == 'back_to_device_choose')
    dp.callback_query.register(handler_back_to_background_color_choose, F.data == 'back_to_background_choose')
    dp.callback_query.register(handler_back_to_primary_text_color_choose, F.data == 'back_to_primary_text_choose')
    dp.callback_query.register(handler_back_to_secondary_text_color_choose, F.data == 'back_to_secondary_text_choose')
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is stop !!!')
