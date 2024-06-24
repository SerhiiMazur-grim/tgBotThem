import os
from PIL import Image

PC_PATH = ('core', 'image', 'pc_theme_layers')
PC_USER_ICON_FILES = [
    'user_icon_1.png', 'user_icon_2.png', 'user_icon_3.png',
    'user_icon_4.png', 'user_icon_5.png', 'user_icon_6.png',
    'user_icon_7.png'
]

PC_IMAGE_LAYER_FILES = [
    'img_bg.png', 'chat_bg.png', 'side_bar.png', 'selected_chat.png',
    'clouds_in.png', 'clouds_out.png', 'prime_txt.png', 'secondary_txt.png',
    'shadows.png'
]

PC_USER_ICON_LIST = []


for filename in PC_USER_ICON_FILES:
    with Image.open(os.path.join(*PC_PATH, filename)) as img:
        user_icon = {
            'size': img.size,
            'alpha': img.split()[3]
        }
        PC_USER_ICON_LIST.append(user_icon)


async def get_pc_layers():
    PC_IMAGE_LAYER_LIST = []

    for filename in PC_IMAGE_LAYER_FILES:
        with Image.open(os.path.join(*PC_PATH, filename)) as image:
            img_data = (pixel for pixel in image.getdata())
            alpha = (pixel for pixel in image.split()[3].getdata())
            image_layer = {
                'img_data': img_data,
                'alpha': alpha,
                'size': image.size
            }
            PC_IMAGE_LAYER_LIST.append(image_layer)
    return PC_IMAGE_LAYER_LIST
