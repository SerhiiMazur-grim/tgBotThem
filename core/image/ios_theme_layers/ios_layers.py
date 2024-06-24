import os
from PIL import Image


IPHONE_PATH = ('core', 'image', 'ios_theme_layers')
IPHONE_IMAGE_LAYER_FILES = [
    'bg.png', 'bg_chat_color_2.png', 'message_clouds_out.png', 'message_clouds_in.png',
    'prime_txt.png', 'second_txt.png', 'shadow.png'
]


async def get_ios_layers():
    IPHONE_IMAGE_LAYER_LIST = []

    # Завантаження шарів зображень
    for filename in IPHONE_IMAGE_LAYER_FILES:
        with Image.open(os.path.join(*IPHONE_PATH, filename)) as image:
            img_data = (pixel for pixel in image.getdata())
            alpha = (pixel for pixel in image.split()[3].getdata())
            image_layer = {
                'img_data': img_data,
                'alpha': alpha,
                'size': image.size
            }
            IPHONE_IMAGE_LAYER_LIST.append(image_layer)
    return IPHONE_IMAGE_LAYER_LIST
