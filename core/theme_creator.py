import os

from android.atdroid_theme import create_android_theme
from desktop.desktop_theme import create_pc_theme
from ios.iphone_theme import create_iphone_theme


async def is_dark_color(hex_color):
    # Видаляємо символ '#' з початку рядка (якщо він там є)
    hex_color = hex_color.lstrip('#')

    # Конвертуємо hex-рядок у значення RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Обчислюємо яскравість за допомогою середнього значення RGB
    brightness = sum(rgb) / 3

    # Якщо яскравість менше деякого порогового значення (наприклад, 128), то колір вважається темним
    threshold = 128
    return brightness < threshold


async def create_theme(user_data, chat_id):
    device = user_data['device']
    image_path = os.path.join('download_photo', user_data["image_name"])

    if device == 'android':
        android_theme = await create_android_theme(
                             chat_id=chat_id,
                             image_path=image_path,
                             bg=user_data['background_color'],
                             primary_txt=user_data['primary_text_color'],
                             secondary_txt=user_data['secondary_text_color'],
                             alfa=user_data['background_alfa'])
        return android_theme

    elif device == 'iphone':

        is_dark = await is_dark_color(user_data['background_color'])

        if is_dark:
            dark = 'true'
            status_bar = 'black'
        else:
            dark = 'false'
            status_bar = 'white'

        iphone_theme = await create_iphone_theme(
                            chat_id=chat_id,
                            image_path=image_path,
                            bg=user_data['background_color'],
                            dark=dark,
                            status_bar=status_bar,
                            primary_txt=user_data['primary_text_color'],
                            not_primary_txt=user_data['secondary_text_color'],
        )
        return iphone_theme

    else:
        pc_theme = await create_pc_theme(
                            chat_id=chat_id,
                            image_path=image_path,
                            background_color=user_data['background_color'],
                            primary_text_color=user_data['primary_text_color'],
                            secondary_text_color=user_data['secondary_text_color'],
                            background_alfa=user_data['background_alfa']
        )
        return pc_theme
