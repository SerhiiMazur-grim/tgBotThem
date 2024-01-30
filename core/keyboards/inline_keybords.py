from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import messages
from config.categories import CATEGORIES, CATEGORIES_GET, DRVICES, DRVICES_GET, CATEGORIES_LANGUAGES, \
    CATEGORIES_LANGUAGES_GET, DRVICES_LANGUAGES_GET


def subscribe_keyboard(checked_channels):
    keyboard = InlineKeyboardBuilder()
    counter = 1

    for channel_id in checked_channels:
        keyboard.button(text=f"{messages.MESSAGE_WITH_CHAT}{counter}", url=f"https://t.me/{channel_id[1:]}")
        counter += 1
    keyboard.button(text=messages.MESSAGE_CHECK_SUBSCRIBE, callback_data='sub_check')
    keyboard.adjust(2, 2, 1)
    return keyboard.as_markup()


def choose_device_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=messages.ANDROID, callback_data='device_android')
    keyboard.button(text=messages.IPHONE, callback_data='device_iphone')
    keyboard.button(text=messages.PC, callback_data='device_desktop')
    keyboard.button(text=messages.ABORT, callback_data='abort')

    keyboard.adjust(1)

    return keyboard.as_markup()


def choose_background_color_keyboard(colors_list):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_1, callback_data=f"background_color_1_{colors_list[0]}")
    keyboard.button(text=messages.BUTTON_2, callback_data=f"background_color_2_{colors_list[1]}")
    keyboard.button(text=messages.BUTTON_3, callback_data=f"background_color_3_{colors_list[2]}")
    keyboard.button(text=messages.BUTTON_4, callback_data=f"background_color_4_{colors_list[3]}")
    keyboard.button(text=messages.BUTTON_5, callback_data=f"background_color_5_{colors_list[4]}")

    keyboard.button(text=messages.BUTTON_WHITE, callback_data='background_color_#ffffff')
    keyboard.button(text=messages.BUTTON_BLACK, callback_data='background_color_#000000')
    keyboard.button(text=messages.BUTTON_AUTO, callback_data='auto_background_color')
    keyboard.button(text=messages.BUTTON_BACK_IKB, callback_data='back_to_device_choose')
    keyboard.button(text=messages.ABORT, callback_data='abort')

    keyboard.adjust(5, 3, 2)

    return keyboard.as_markup()


def choose_primary_text_color_keyboard(colors_list):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_1, callback_data=f"primary_text_color_1_{colors_list[0]}")
    keyboard.button(text=messages.BUTTON_2, callback_data=f"primary_text_color_2_{colors_list[1]}")
    keyboard.button(text=messages.BUTTON_3, callback_data=f"primary_text_color_3_{colors_list[2]}")
    keyboard.button(text=messages.BUTTON_4, callback_data=f"primary_text_color_4_{colors_list[3]}")
    keyboard.button(text=messages.BUTTON_5, callback_data=f"primary_text_color_5_{colors_list[4]}")

    keyboard.button(text=messages.BUTTON_WHITE, callback_data='primary_text_color_#ffffff')
    keyboard.button(text=messages.BUTTON_BLACK, callback_data='primary_text_color_#000000')
    keyboard.button(text=messages.BUTTON_BACK_IKB, callback_data='back_to_background_choose')
    keyboard.button(text=messages.ABORT, callback_data='abort')

    keyboard.adjust(5, 3, 1)

    return keyboard.as_markup()


def choose_secondary_text_color_keyboard(colors_list):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_1, callback_data=f"secondary_text_color_1_{colors_list[0]}")
    keyboard.button(text=messages.BUTTON_2, callback_data=f"secondary_text_color_2_{colors_list[1]}")
    keyboard.button(text=messages.BUTTON_3, callback_data=f"secondary_text_color_3_{colors_list[2]}")
    keyboard.button(text=messages.BUTTON_4, callback_data=f"secondary_text_color_4_{colors_list[3]}")
    keyboard.button(text=messages.BUTTON_5, callback_data=f"secondary_text_color_5_{colors_list[4]}")

    keyboard.button(text=messages.BUTTON_WHITE, callback_data='secondary_text_color_#ffffff')
    keyboard.button(text=messages.BUTTON_BLACK, callback_data='secondary_text_color_#000000')
    keyboard.button(text=messages.BUTTON_BACK_IKB, callback_data='back_to_primary_text_choose')
    keyboard.button(text=messages.ABORT, callback_data='abort')

    keyboard.adjust(5, 3, 1)

    return keyboard.as_markup()


def choose_alfa_background_color_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_ALFA_10, callback_data="background_alfa_a10")
    keyboard.button(text=messages.BUTTON_ALFA_20, callback_data="background_alfa_a20")
    keyboard.button(text=messages.BUTTON_ALFA_30, callback_data="background_alfa_a30")
    keyboard.button(text=messages.BUTTON_ALFA_40, callback_data="background_alfa_a40")
    keyboard.button(text=messages.BUTTON_ALFA_50, callback_data="background_alfa_a50")
    keyboard.button(text=messages.BUTTON_ALFA_60, callback_data="background_alfa_a60")
    keyboard.button(text=messages.BUTTON_ALFA_70, callback_data="background_alfa_a70")
    keyboard.button(text=messages.BUTTON_ALFA_80, callback_data="background_alfa_a80")
    keyboard.button(text=messages.BUTTON_ALFA_90, callback_data="background_alfa_a90")

    keyboard.button(text=messages.BUTTON_ALFA_0, callback_data='background_alfa_a0')
    keyboard.button(text=messages.BUTTON_BACK_IKB, callback_data='back_to_secondary_text_choose')
    keyboard.button(text=messages.ABORT, callback_data='abort')

    keyboard.adjust(3, 3, 3, 1, 2)

    return keyboard.as_markup()


def add_bot_to_chat_inl_keyboard():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=messages.BUTTON_ADD_BOT_TO_CHAT, url='t.me/Grimm_Python_Test_Bot?startgroup&admin=post_messages')
    keyboard.adjust(1)
    
    return keyboard.as_markup()


def admin_add_theme_category_ikb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=messages.IKB_BUTTON_ADMIN_ADD_THEME_CATEGORY,
                    callback_data='admin_add_theme_cat')
    keyboard.button(text=messages.IKB_BUTTON_ADMIN_DEL_THEME_CATEGORY,
                    callback_data='admin_del_theme_cat')
    keyboard.adjust(2)
    return keyboard.as_markup()


def admin_add_language_category_ikb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=messages.IKB_BUTTON_ADMIN_ADD_LANGUAGE_CATEGORY,
                    callback_data='admin_add_language_cat')
    keyboard.button(text=messages.IKB_BUTTON_ADMIN_DEL_LANGUAGE_CATEGORY,
                    callback_data='admin_del_language_cat')
    keyboard.adjust(2)
    return keyboard.as_markup()


def admin_del_theme_category_ikb(categories):
    keyboard = InlineKeyboardBuilder()
    
    for cat in categories:
        keyboard.button(text=cat.title, callback_data=f'del_theme_cat_{cat.id}')
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def admin_del_language_category_ikb(categories):
    keyboard = InlineKeyboardBuilder()
    
    for cat in categories:
        keyboard.button(text=cat.title, callback_data=f'del_language_cat_{cat.id}')
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def choice_category_ikb_keyboard(categories):
    keyboard = InlineKeyboardBuilder()

    for cat in categories:
        keyboard.button(text=cat.title, callback_data=f'add_theme_cat_{cat.id}')
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def choice_category_lang_ikb(categories):
    keyboard = InlineKeyboardBuilder()

    for cat in categories:
        keyboard.button(text=cat.title, callback_data=f'add_lang_cat_{cat.id}')
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def abort_add_theme_ikb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=messages.BUTTON_ABORT_ADD_THEME, callback_data='abort_add_theme')
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def choice_device_db_ikb_keyboard():
    keyboard = InlineKeyboardBuilder()

    for device, value in DRVICES.items():
        keyboard.button(text=device, callback_data=value)
    keyboard.button(text=messages.BUTTON_ABORT_ADD_THEME, callback_data='abort_add_theme')
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def choice_device_db_get_ikb():
    keyboard = InlineKeyboardBuilder()

    for device, value in DRVICES.items():
        keyboard.button(text=device, callback_data=value)
    
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def choice_category_db_get_ikb(categories):
    keyboard = InlineKeyboardBuilder()

    for cat in categories:
        keyboard.button(text=cat.title, callback_data=f'get_theme_cat_{cat.id}')
        
    keyboard.adjust(3)
    return keyboard.as_markup()


def send_post_ikb():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_SEND_TO_ALL, callback_data='post_send_all')
    keyboard.button(text=messages.BUTTON_SEND_TO_PRIVATE, callback_data='post_send_private')
    keyboard.button(text=messages.BUTTON_SEND_TO_GROUP, callback_data='post_send_group')
    keyboard.button(text=messages.BUTTON_CREATE_LIMITED_POST, callback_data='create_limited_post')
    keyboard.button(text=messages.BUTTON_DELETE_POST, callback_data='post_delete')
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def start_create_post_ikb():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_ABORT_CREATE_POST, callback_data='abort_create_post')
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def abort_create_limited_post_ikb():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_ABORT_CREATE_POST, callback_data='abort_create_post')
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def abort_sending_limited_post_ikb():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=messages.BUTTON_STOP_SENDING_POST, callback_data='abort_sending_limited_post')
    keyboard.button(text=messages.BUTTON_ABORT_CREATE_POST, callback_data='abort_create_post')
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def send_limited_post_ikb():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=messages.BUTTON_SEND_LIMITED_POST, callback_data='send_limited_post')
    keyboard.button(text=messages.BUTTON_DELETE_POST, callback_data='post_delete')
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def fonts_ikb():
    keyboard = InlineKeyboardBuilder()

    for view, font in messages.FONTS_BUTTONS.items():
        keyboard.button(text=view, callback_data=font)
    keyboard.adjust(2)
    return keyboard.as_markup()


def language_categories_ikb():
    keyboard = InlineKeyboardBuilder()
    
    for category, index in CATEGORIES_LANGUAGES.items():
        keyboard.button(text=category, callback_data=index)
    keyboard.adjust(3)
    return keyboard.as_markup()


def choice_device_lang_get_ikb():
    keyboard = InlineKeyboardBuilder()

    for device, value in DRVICES.items():
        keyboard.button(text=device, callback_data=value)
    
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def choice_category_lang_db_get_ikb(categories):
    keyboard = InlineKeyboardBuilder()

    for cat in categories:
        keyboard.button(text=cat.title, callback_data=f'get_language_cat_{cat.id}')
    
    keyboard.adjust(3)
    return keyboard.as_markup()


def active_statistic_menu_ikb():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=messages.BUTTON_DAY_ACTIVITY, callback_data='day_activity')
    keyboard.button(text=messages.BUTTON_WEEK_ACTIVITY, callback_data='week_activity')
    keyboard.button(text=messages.BUTTON_MONTH_ACTIVITY, callback_data='month_activity')
    
    keyboard.adjust(1)
    return keyboard.as_markup()
