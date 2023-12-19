from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import messages
from core.utils import is_admin


def user_keyboard(user_id):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_CREATE_THEME)
    keyboard.button(text=messages.BUTTON_ADD_TO_CHAT)
    keyboard.button(text=messages.BUTTON_THEME_CATALOG)
    keyboard.button(text=messages.BUTTON_FONTS_CATALOG)
    keyboard.button(text=messages.BUTTON_FAQ)
    
    if is_admin(user_id):
        keyboard.button(text=messages.BUTTON_ADMIN)
    
    keyboard.adjust(2, 2, 1, 1)
    
    return keyboard.as_markup(resize_keyboard=True)


def admin_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_ADD_THEME)
    keyboard.button(text=messages.BUTTON_ADD_FONT)
    keyboard.button(text=messages.BUTTON_CREATE_MAILING)
    keyboard.button(text=messages.BUTTON_VIEW_MAILING)
    keyboard.button(text=messages.BUTTON_BACK_TO_USER_KB)
    keyboard.adjust(2, 2, 1)
    
    return keyboard.as_markup(resize_keyboard=True)


def nex_themes_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_NEXT_THEMES)
    keyboard.button(text=messages.BUTTON_BACK)
    keyboard.adjust(1)
    
    return keyboard.as_markup(resize_keyboard=True)
