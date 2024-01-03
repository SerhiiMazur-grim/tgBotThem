import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from config.api_keys import TOKEN_API
from config import messages
from core.handlers import basic, theme_handlers, language_handlers, \
theme_catalog_handlers, mailing_handlers, fonts_handlers
from core.middleware import CleanupMiddleware, PostSenderMiddleware, IsSubscribedMiddleware, check_and_delete_files
from core.utils import start_bot, sub_checker
from core.filters import IsAdminFilter, IsPrivateChatFilter
from core.states import AddThemeState, GetThemesCatalogState, GetFontTextState, AddLanguageState


async def main():
    await check_and_delete_files()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN_API)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()

    dp.message.middleware.register(CleanupMiddleware())
    dp.message.middleware.register(PostSenderMiddleware(bot))
    dp.message.middleware.register(IsSubscribedMiddleware(bot))
    
    # basic handlers
    dp.startup.register(start_bot)
    dp.message.register(basic.command_start, Command('start'))
    dp.message.register(basic.command_admin_kb, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADMIN)
    dp.message.register(basic.command_create_theme, IsPrivateChatFilter(), F.text == messages.BUTTON_CREATE_THEME)
    dp.message.register(basic.command_add_to_chat, IsPrivateChatFilter(), F.text == messages.BUTTON_ADD_TO_CHAT)
    dp.message.register(basic.command_faq, IsPrivateChatFilter(), F.text == messages.BUTTON_FAQ)
    dp.callback_query.register(sub_checker, F.data == 'sub_check')
    
    # language handlers
    dp.message.register(language_handlers.get_catalog_languages, IsPrivateChatFilter(), F.text == messages.BUTTON_LANGUAGE_CATALOG)
    dp.callback_query.register(language_handlers.get_device_catalog_languages, F.data.startswith('dev_lang_get_'))
    dp.callback_query.register(language_handlers.get_category_catalog_themes, F.data.startswith('lang_cat_get_'))
    dp.message.register(language_handlers.get_next_languages, IsPrivateChatFilter(), F.text == messages.BUTTON_NEXT_LANGUAGES)
    dp.message.register(language_handlers.go_to_main_menu_from_lang_catalog, IsPrivateChatFilter(), F.text == messages.BUTTON_BACK_FROM_LANG_CAT)
    dp.message.register(language_handlers.start_add_language, IsAdminFilter(), IsPrivateChatFilter(),
                        F.text == messages.BUTTON_ADD_LANGUAGE)
    dp.poll_answer.register(language_handlers.add_language_device, AddLanguageState.device)
    dp.callback_query.register(language_handlers.add_language_category, AddLanguageState.category)
    dp.message.register(language_handlers.add_previev_and_desc_for_language, IsAdminFilter(), IsPrivateChatFilter(),
                        AddLanguageState.preview)
    # dp.message.register(language_handlers.add_preview_for_language, IsAdminFilter(), IsPrivateChatFilter(), F.media_group_id)
    
    # fonts handlers
    dp.message.register(fonts_handlers.font_catalog, IsPrivateChatFilter(), F.text == messages.BUTTON_FONTS_CATALOG)
    dp.message.register(fonts_handlers.get_text_from_user, IsPrivateChatFilter(), GetFontTextState.text)
    dp.callback_query.register(fonts_handlers.change_font_in_text, F.data.startswith('font_'))
    
    # mailing handlers
    dp.message.register(mailing_handlers.create_mailing, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_CREATE_MAILING)
    dp.callback_query.register(mailing_handlers.start_limited_post, F.data == 'create_limited_post')
    dp.callback_query.register(mailing_handlers.abort_sending_limit_post, F.data == 'abort_sending_limited_post')
    dp.message.register(mailing_handlers.init_limited_post, IsAdminFilter(), IsPrivateChatFilter(), F.text.startswith('USERS'))
    dp.message.register(mailing_handlers.forward_post_message,
                        IsAdminFilter(), IsPrivateChatFilter(), (F.forward_from | F.forward_from_chat) & ~F.media_group_id)
    dp.message.register(mailing_handlers.save_media_group_post_media, 
                        IsAdminFilter(), IsPrivateChatFilter(),
                        (F.caption.startswith('POST\n') | F.text.startswith('POST\n')) | ((F.forward_from | F.forward_from_chat) & F.media_group_id))
    dp.message.register(mailing_handlers.view_post_media, IsAdminFilter(), IsPrivateChatFilter(),
                        F.text == messages.BUTTON_VIEW_MAILING)
    dp.callback_query.register(mailing_handlers.send_limited_post, F.data == 'send_limited_post')
    dp.callback_query.register(mailing_handlers.send_post_to_all, F.data == 'post_send_all')
    dp.callback_query.register(mailing_handlers.send_post_to_private, F.data == 'post_send_private')
    dp.callback_query.register(mailing_handlers.send_post_to_group, F.data == 'post_send_group')
    dp.callback_query.register(mailing_handlers.delete_post, F.data == 'post_delete')
    dp.callback_query.register(mailing_handlers.abort_create_post, F.data == 'abort_create_post')
    
    # theme catalog handlers
    dp.message.register(theme_catalog_handlers.get_catalog_themes, IsPrivateChatFilter(), F.text == messages.BUTTON_THEME_CATALOG)
    dp.message.register(theme_catalog_handlers.go_to_main_menu, IsPrivateChatFilter(), F.text == messages.BUTTON_BACK)
    dp.message.register(theme_catalog_handlers.get_next_themes, IsPrivateChatFilter(), F.text == messages.BUTTON_NEXT_THEMES)
    dp.callback_query.register(theme_catalog_handlers.get_device_catalog_themes, GetThemesCatalogState.device)
    dp.callback_query.register(theme_catalog_handlers.get_category_catalog_themes, GetThemesCatalogState.category)
    #----------------------------------------------------------------------------------------------------------------
    dp.message.register(theme_catalog_handlers.start_add_theme, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADD_THEME)
    dp.callback_query.register(theme_catalog_handlers.abort_add_theme, F.data == 'abort_add_theme')
    dp.callback_query.register(theme_catalog_handlers.add_theme_device, AddThemeState.device)
    dp.message.register(theme_catalog_handlers.add_theme_preview, IsPrivateChatFilter(), AddThemeState.preview)
    dp.message.register(theme_catalog_handlers.add_theme_file, IsPrivateChatFilter(), AddThemeState.file)
    dp.callback_query.register(theme_catalog_handlers.add_theme_category,  AddThemeState.category)
      
    # theme handlers
    dp.message.register(theme_handlers.command_user_kb, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_BACK_TO_USER_KB)
    dp.message.register(theme_handlers.handle_photo, F.photo | F.document)
    dp.callback_query.register(theme_handlers.handler_abort, F.data == 'abort')
    dp.callback_query.register(theme_handlers.handler_device, F.data.startswith('device_'))
        
    dp.callback_query.register(theme_handlers.handler_background_color, F.data.startswith('background_color_'))
    dp.callback_query.register(theme_handlers.handler_primary_text_color, F.data.startswith('primary_text_color_'))
    dp.callback_query.register(theme_handlers.handler_secondary_text_color, F.data.startswith('secondary_text_color_'))
    dp.callback_query.register(theme_handlers.handler_alfa_background_color, F.data.startswith('background_alfa_'))
    dp.callback_query.register(theme_handlers.handler_auto_theme, F.data == 'auto_background_color')

    dp.callback_query.register(theme_handlers.handler_back_to_device_choose, F.data == 'back_to_device_choose')
    dp.callback_query.register(theme_handlers.handler_back_to_background_color_choose, F.data == 'back_to_background_choose')
    dp.callback_query.register(theme_handlers.handler_back_to_primary_text_color_choose, F.data == 'back_to_primary_text_choose')
    dp.callback_query.register(theme_handlers.handler_back_to_secondary_text_color_choose, F.data == 'back_to_secondary_text_choose')
    
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is stop !!!')
