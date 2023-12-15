from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import messages


def user_keyboard(user_id, admin_list):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_CREATE_THEME)
    keyboard.button(text=messages.BUTTON_ADD_TO_CHAT)
    keyboard.button(text=messages.BUTTON_THEME_CATALOG)
    keyboard.button(text=messages.BUTTON_FONTS_CATALOG)
    keyboard.button(text=messages.BUTTON_FAQ)
    
    if str(user_id) in admin_list:
        keyboard.button(text=messages.BUTTON_ADD_THEME)
        keyboard.button(text=messages.BUTTON_ADD_FONT)
    
    keyboard.adjust(2, 2, 1, 2)
    
    return keyboard.as_markup()
