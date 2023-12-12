from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import messages


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
    keyboard.button(text=messages.BUTTON_BACK, callback_data='back_to_device_choose')
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
    keyboard.button(text=messages.BUTTON_BACK, callback_data='back_to_background_choose')
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
    keyboard.button(text=messages.BUTTON_BACK, callback_data='back_to_primary_text_choose')
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
    keyboard.button(text=messages.BUTTON_BACK, callback_data='back_to_secondary_text_choose')
    keyboard.button(text=messages.ABORT, callback_data='abort')

    keyboard.adjust(3, 3, 3, 1, 2)

    return keyboard.as_markup()
