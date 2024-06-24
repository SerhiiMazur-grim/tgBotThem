import os
from PIL import Image

ANDROID_PATH = ('core', 'image', 'android_theme_layers')
ANDROID_USER_ICON_FILES = [
    'user_icon_1.png', 'user_icon_2.png', 'user_icon_3.png', 'user_icon_4.png',
    'user_icon_5.png', 'user_icon_6.png', 'user_icon_7.png', 'user_icon_8.png'
]
ANDROID_IMAGE_LAYER_FILES = [
    'bg.png', 'bg_chat_color_2.png', 'message_clouds_out.png', 'message_clouds_in.png',
    'prime_txt.png', 'second_txt.png', 'shadow.png'
]

ANDROID_USER_ICON_LIST = []

# Завантаження користувацьких іконок
for filename in ANDROID_USER_ICON_FILES:
    with Image.open(os.path.join(*ANDROID_PATH, filename)) as img:
        user_icon = {
            'size': img.size,
            'alpha': img.split()[3]
        }
        ANDROID_USER_ICON_LIST.append(user_icon)


async def get_android_layers():
    ANDROID_IMAGE_LAYER_LIST = []
    # Завантаження шарів зображень
    for filename in ANDROID_IMAGE_LAYER_FILES:
        with Image.open(os.path.join(*ANDROID_PATH, filename)) as image:
            img_data = (pixel for pixel in image.getdata())
            alpha = (pixel for pixel in image.split()[3].getdata())
            image_layer = {
                'img_data': img_data,
                'alpha': alpha,
                'size': image.size
            }
            ANDROID_IMAGE_LAYER_LIST.append(image_layer)
    return ANDROID_IMAGE_LAYER_LIST