import os
from PIL import Image, ImageDraw, ImageFont

from config.messages import PREVIEW_WATER_MARK
from core.utils import hex_to_rgba_v2


with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'bg.png')) as image:
    IMAGE_LAYER_1 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'bg_chat_color_2.png')) as image:
    IMAGE_LAYER_2 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'message_clouds_out.png')) as image:
    IMAGE_LAYER_3 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'message_clouds_in.png')) as image:
    IMAGE_LAYER_4 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'prime_txt.png')) as image:
    IMAGE_LAYER_5 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'second_txt.png')) as image:
    IMAGE_LAYER_6 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'shadow.png')) as image:
    IMAGE_LAYER_7 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }


async def crop_wallpaper(wallpaper_path):
    with Image.open(wallpaper_path) as img:
        width, height = img.size
        
        if width > int(height*0.7):
            top_x = width//2 - int(height*0.7)//2
            top_y = 0
            bot_x = width//2 + int(height*0.7)//2
            bot_y = height
            
        else:
            top_x = 0
            top_y = height//2 - int(width//0.7)//2
            bot_x = width
            bot_y = height//2 + int(width//0.7)//2

        cropped_img = img.crop((top_x, top_y, bot_x, bot_y))
    new_width = int((750 / cropped_img.size[1]) * cropped_img.size[0])
    wallpaper = cropped_img.resize((new_width, 750))
    
    return wallpaper


async def set_color_v2(images, colors):
    layers = []
    for image, color in zip(images, colors):
        img_data = image['img_data']
        alpha_channel = image['alpha']

        if len(color) == 4:
            new_img_data = [
                (color[0], color[1], color[2],  color[3]) if alpha > 0 else pixel
                for pixel, alpha in zip(img_data, alpha_channel)
            ]
        else:
            new_img_data = [
            (color[0], color[1], color[2],  alpha) if alpha > 0 else pixel
            for pixel, alpha in zip(img_data, alpha_channel)
            ]

        new_img = Image.new("RGBA", image['size'])
        new_img.putdata([tuple(p) for p in new_img_data])
        layers.append(new_img)

    return layers


async def create_ios_preview(chat_id, photo, preview_bg, bg, primary_txt,
                              secondary_txt, chat_in):
    background = Image.new('RGB', (1088, 1088), 'white')

    layers = []
    wallpaper = await crop_wallpaper(photo)
    images = [
        IMAGE_LAYER_1,
        IMAGE_LAYER_2,
        IMAGE_LAYER_3,
        IMAGE_LAYER_4,
        IMAGE_LAYER_5,
        IMAGE_LAYER_6,
        IMAGE_LAYER_7,
    ]
    
    colors = await hex_to_rgba_v2([
        preview_bg,
        bg,
        bg,
        chat_in,
        primary_txt,
        secondary_txt,
        chat_in
    ])

    
    assets = await set_color_v2(images, colors)
    layers.extend(i for i in assets)
    
    background.paste(wallpaper, (45, 155))
    
    for layer in layers:
        background.paste(layer, (0, 0), layer)
    
    with Image.open(os.path.join('core', 'image', 'ios_theme_layers', 'user_icons.png')) as img:
        background.paste(img, (0, 0), img)
    
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("arial.ttf", 20)
    text_color = colors[1]
    position = (40, 1015)

    draw.text(position, PREVIEW_WATER_MARK, font=font, fill=text_color)
    
    preview = os.path.join('ios', 'theme', str(chat_id), 'preview.jpg')
    
    background.save(preview)
    
    return preview
