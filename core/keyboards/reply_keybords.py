from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import messages
from config.api_keys import ADMINS


def user_keyboard(user_id):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_CREATE_THEME)
    keyboard.button(text=messages.BUTTON_ADD_TO_CHAT)
    keyboard.button(text=messages.BUTTON_THEME_CATALOG)
    keyboard.button(text=messages.BUTTON_LANGUAGE_CATALOG)
    keyboard.button(text=messages.BUTTON_FONTS_CATALOG)
    keyboard.button(text=messages.BUTTON_FAQ)
    
    if str(user_id) in ADMINS:
        keyboard.button(text=messages.BUTTON_ADMIN)
    
    keyboard.adjust(2, 2, 2, 1)
    
    return keyboard.as_markup(resize_keyboard=True)


def admin_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_ADMIN_THEME_CATALOG)
    keyboard.button(text=messages.BUTTON_ADMIN_LANGUAGE_CATALOG)
    keyboard.button(text=messages.BUTTON_CREATE_MAILING)
    keyboard.button(text=messages.BUTTON_VIEW_MAILING)
    keyboard.button(text=messages.BUTTON_BACKUP)
    keyboard.button(text=messages.BUTTON_BACK_TO_USER_KB)
    keyboard.adjust(2, 2, 2)
    
    return keyboard.as_markup(resize_keyboard=True)


def admin_theme_catalog_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_ADMIN_THEME_CATEGORY)
    keyboard.button(text=messages.BUTTON_ADD_THEME)
    keyboard.button(text=messages.BUTTON_ADMIN)
    keyboard.adjust(1)
    
    return keyboard.as_markup(resize_keyboard=True)


def nex_themes_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_NEXT_THEMES)
    keyboard.button(text=messages.BUTTON_BACK)
    keyboard.adjust(1)
    
    return keyboard.as_markup(resize_keyboard=True)


def catalog_theme_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_BACK)
    keyboard.adjust(1)
    
    return keyboard.as_markup(resize_keyboard=True)


def catalog_language_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_BACK_FROM_LANG_CAT)
    keyboard.adjust(1)
    
    return keyboard.as_markup(resize_keyboard=True)


def nex_languages_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_NEXT_LANGUAGES)
    keyboard.button(text=messages.BUTTON_BACK_FROM_LANG_CAT)
    keyboard.adjust(1)
    
    return keyboard.as_markup(resize_keyboard=True)
