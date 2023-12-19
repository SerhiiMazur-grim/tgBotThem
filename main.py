import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, and_f, invert_f

from config.api_keys import TOKEN_API
from config import messages
from core.handlers import basic, theme_handlers, theme_catalog_handlers, mailing_handlers
from core.middleware import CleanupMiddleware, check_and_delete_files
from core.utils import start_bot, sub_checker


async def main():
    await check_and_delete_files()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN_API, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()

    dp.message.middleware.register(CleanupMiddleware())
    
    # basic handlers
    dp.startup.register(start_bot)
    dp.message.register(basic.command_start, Command('start'))
    dp.message.register(basic.command_admin_kb, F.text == messages.BUTTON_ADMIN)
    dp.message.register(basic.command_create_theme, F.text == messages.BUTTON_CREATE_THEME)
    dp.message.register(basic.command_add_to_chat, F.text == messages.BUTTON_ADD_TO_CHAT)
    dp.message.register(basic.command_faq, F.text == messages.BUTTON_FAQ)
    dp.callback_query.register(sub_checker, F.data == 'sub_check')

    dp.message.register(mailing_handlers.create_mailing, F.text == messages.BUTTON_CREATE_MAILING)
    dp.message.register(mailing_handlers.save_post_media, F.media_group_id | F.caption.startswith('POST\n'))
    dp.message.register(mailing_handlers.view_post_media, F.text == messages.BUTTON_VIEW_MAILING)
    dp.callback_query.register(mailing_handlers.send_post_to_all, F.data == 'post_send_all')
    
    
    # theme handlers
    dp.message.register(theme_handlers.command_user_kb, F.text == messages.BUTTON_BACK_TO_USER_KB)
    dp.message.register(theme_handlers.start_add_theme, F.text == messages.BUTTON_ADD_THEME)
    dp.message.register(theme_handlers.handle_photo, F.photo)
    dp.message.register(theme_handlers.handle_photo, F.document)
    dp.callback_query.register(theme_handlers.add_theme_category, F.data.startswith('cat_'))
    dp.callback_query.register(theme_handlers.handler_abort, F.data == 'abort')
    dp.callback_query.register(theme_handlers.handler_device, F.data.startswith('device_'))
    dp.callback_query.register(theme_handlers.add_theme_device, F.data.startswith('db-dev_'))
    dp.callback_query.register(theme_handlers.handler_background_color, F.data.startswith('background_color_'))
    dp.callback_query.register(theme_handlers.handler_primary_text_color, F.data.startswith('primary_text_color_'))
    dp.callback_query.register(theme_handlers.handler_secondary_text_color, F.data.startswith('secondary_text_color_'))
    dp.callback_query.register(theme_handlers.handler_alfa_background_color, F.data.startswith('background_alfa_'))
    dp.callback_query.register(theme_handlers.handler_auto_theme, F.data == 'auto_background_color')

    dp.callback_query.register(theme_handlers.handler_back_to_device_choose, F.data == 'back_to_device_choose')
    dp.callback_query.register(theme_handlers.handler_back_to_background_color_choose, F.data == 'back_to_background_choose')
    dp.callback_query.register(theme_handlers.handler_back_to_primary_text_color_choose, F.data == 'back_to_primary_text_choose')
    dp.callback_query.register(theme_handlers.handler_back_to_secondary_text_color_choose, F.data == 'back_to_secondary_text_choose')
    
    # catalog handlers
    dp.message.register(theme_catalog_handlers.get_catalog_themes, F.text == messages.BUTTON_THEME_CATALOG)
    dp.message.register(theme_catalog_handlers.go_to_main_menu, F.text == messages.BUTTON_BACK)
    dp.message.register(theme_catalog_handlers.get_next_themes, F.text == messages.BUTTON_NEXT_THEMES)
    dp.callback_query.register(theme_catalog_handlers.get_device_catalog_themes, F.data.startswith('db-get-device_'))
    dp.callback_query.register(theme_catalog_handlers.get_category_catalog_themes, F.data.startswith('db-get-cat_'))
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is stop !!!')
