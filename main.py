import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation

from database import create_sessionmaker
import middlewares
from config.api_keys import TOKEN_API, DATA_BASE_URL
from config import messages
from core.handlers import basic, theme_handlers, language_handlers, \
theme_catalog_handlers, fonts_handlers, posts_handlers
from core.middleware import CleanupMiddleware, PostSenderMiddleware, IsSubscribedMiddleware, check_and_delete_files
from core.utils import sub_checker
from core.filters import IsAdminFilter, IsPrivateChatFilter
from core.states import AddThemeState, GetThemesCatalogState, GetFontTextState, \
    AddLanguageState, GetLanguageCatalogState, AddPostState, AddThemeCat, AddLanguageCat
from statistica import base_statistic_handler, user_activity_statistica, full_statistica, referal_statistica


logger = logging.getLogger(__name__)


async def main():
    await check_and_delete_files()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        stream=sys.stdout)
    logger.info("Starting bot...")
    
    storage = MemoryStorage()
    sessionmaker = await create_sessionmaker(DATA_BASE_URL)
    
    bot = Bot(token=TOKEN_API)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
    middlewares.setup(dp, sessionmaker)

    dp.message.middleware.register(CleanupMiddleware())
    dp.message.middleware.register(PostSenderMiddleware(bot))
    dp.message.middleware.register(IsSubscribedMiddleware(bot))
        
    # basic handlers
    # dp.startup.register(start_bot)
    dp.message.register(basic.command_start, Command('start'))
    dp.message.register(basic.command_admin_kb, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADMIN)
    dp.message.register(basic.command_user_kb, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_BACK_TO_USER_KB)
    dp.message.register(basic.command_create_theme, IsPrivateChatFilter(), F.text == messages.BUTTON_CREATE_THEME)
    dp.message.register(basic.command_add_to_chat, IsPrivateChatFilter(), F.text == messages.BUTTON_ADD_TO_CHAT)
    dp.message.register(basic.command_faq, IsPrivateChatFilter(), F.text == messages.BUTTON_FAQ)
    dp.callback_query.register(sub_checker, F.data == 'sub_check')

    # backup handler
    # dp.message.register(backup_handlers.get_backup, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_BACKUP)
    
    # statistica handlers
    dp.message.register(base_statistic_handler.statistic_menu, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_STATISTIC_MENU)
    dp.message.register(base_statistic_handler.active_statistic_menu, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ACTIVE_STATISTICA)
    dp.message.register(base_statistic_handler.referals_statistic_menu, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_REFERAL_STATISTICA)
    dp.callback_query.register(user_activity_statistica.user_activity_per_day, IsAdminFilter(), F.data=='day_activity')
    dp.callback_query.register(user_activity_statistica.user_activity_per_week, IsAdminFilter(), F.data=='week_activity')
    dp.callback_query.register(user_activity_statistica.user_activity_per_month, IsAdminFilter(), F.data=='month_activity')
    dp.message.register(full_statistica.get_full_statistica, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_FULL_STATISTICA)
    dp.callback_query.register(referal_statistica.detail_referal_statistica, IsAdminFilter(), F.data.startswith('ref_title_'))
    
    # language handlers
    dp.message.register(language_handlers.admin_language_catalog, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADMIN_LANGUAGE_CATALOG)
    dp.message.register(language_handlers.admin_language_category, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADMIN_LANGUAGE_CATEGORY)
    dp.callback_query.register(language_handlers.admin_start_add_language_category, IsAdminFilter(), F.data == 'admin_add_language_cat')
    dp.message.register(language_handlers.admin_get_language_category, AddLanguageCat.category)
    dp.callback_query.register(language_handlers.admin_start_delete_language_category, IsAdminFilter(), F.data == 'admin_del_language_cat')
    dp.callback_query.register(language_handlers.admin_delete_language_category, IsAdminFilter(), F.data.startswith('del_language_cat_'))
    
    #--------------------------------------------------------------------------------------------------
    
    dp.message.register(language_handlers.get_catalog_languages, IsPrivateChatFilter(), F.text == messages.BUTTON_LANGUAGE_CATALOG)
    dp.callback_query.register(language_handlers.get_device_catalog_languages, GetLanguageCatalogState.device)
    dp.callback_query.register(language_handlers.get_category_catalog_themes, GetLanguageCatalogState.category)
    dp.message.register(language_handlers.get_next_languages, IsPrivateChatFilter(), F.text == messages.BUTTON_NEXT_LANGUAGES)
    dp.message.register(language_handlers.go_to_main_menu_from_lang_catalog, IsPrivateChatFilter(), F.text == messages.BUTTON_BACK_FROM_LANG_CAT)
    dp.message.register(language_handlers.start_add_language, IsAdminFilter(), IsPrivateChatFilter(),
                        F.text == messages.BUTTON_ADD_LANGUAGE)
    dp.poll_answer.register(language_handlers.add_language_device, AddLanguageState.device)
    dp.callback_query.register(language_handlers.add_language_category, AddLanguageState.category)
    dp.message.register(language_handlers.add_previev_and_desc_for_language, IsAdminFilter(), IsPrivateChatFilter(),
                        AddLanguageState.preview)
    
    # fonts handlers
    dp.message.register(fonts_handlers.font_catalog, IsPrivateChatFilter(), F.text == messages.BUTTON_FONTS_CATALOG)
    dp.message.register(fonts_handlers.get_text_from_user, IsPrivateChatFilter(), GetFontTextState.text)
    dp.callback_query.register(fonts_handlers.change_font_in_text, F.data.startswith('font_')) 
    
    # mailing handlers
    dp.message.register(posts_handlers.create_mailing, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_CREATE_MAILING)
    dp.message.register(posts_handlers.get_post, IsAdminFilter(), IsPrivateChatFilter(), AddPostState.post)
    dp.message.register(posts_handlers.view_post, IsAdminFilter(), IsPrivateChatFilter(),
                    F.text == messages.BUTTON_VIEW_MAILING)
    dp.callback_query.register(posts_handlers.start_limited_post, F.data == 'create_limited_post')
    dp.message.register(posts_handlers.get_users_count, IsAdminFilter(), IsPrivateChatFilter(), AddPostState.users_count)
    dp.callback_query.register(posts_handlers.send_limited_post, F.data == 'send_limited_post')
    dp.callback_query.register(posts_handlers.delete_post, F.data == 'post_delete')
    dp.callback_query.register(posts_handlers.abort_create_post, F.data == 'abort_create_post')
    dp.callback_query.register(posts_handlers.abort_sending_limit_post, F.data == 'abort_sending_limited_post')
    dp.callback_query.register(posts_handlers.send_post_to_all, F.data == 'post_send_all')
    dp.callback_query.register(posts_handlers.send_post_to_private, F.data == 'post_send_private')
    dp.callback_query.register(posts_handlers.send_post_to_group, F.data == 'post_send_group')
    
    # theme catalog handlers
    dp.message.register(theme_catalog_handlers.admin_theme_catalog, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADMIN_THEME_CATALOG)
    dp.message.register(theme_catalog_handlers.admin_theme_category, IsAdminFilter(), IsPrivateChatFilter(), F.text == messages.BUTTON_ADMIN_THEME_CATEGORY)
    dp.callback_query.register(theme_catalog_handlers.admin_start_add_theme_category, IsAdminFilter(), F.data == 'admin_add_theme_cat')
    dp.message.register(theme_catalog_handlers.admin_get_theme_category, AddThemeCat.category)
    dp.callback_query.register(theme_catalog_handlers.admin_start_delete_theme_category, IsAdminFilter(), F.data == 'admin_del_theme_cat')
    dp.callback_query.register(theme_catalog_handlers.admin_delete_theme_category, IsAdminFilter(), F.data.startswith('del_theme_cat_'))
    
    
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
        await dp.fsm.storage.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
