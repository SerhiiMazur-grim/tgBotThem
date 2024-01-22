import os
from PIL import Image, ImageDraw, ImageFont

from config.messages import PREVIEW_WATER_MARK
from core.utils import hex_to_rgba_v2


with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_1.png')) as img:
    USER_ICON_1 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_2.png')) as img:
    USER_ICON_2 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_3.png')) as img:
    USER_ICON_3 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_4.png')) as img:
    USER_ICON_4 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_5.png')) as img:
    USER_ICON_5 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_6.png')) as img:
    USER_ICON_6 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_7.png')) as img:
    USER_ICON_7 = {
        'size': img.size,
        'alpha': img.split()[3]
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'user_icon_8.png')) as img:
    USER_ICON_8 = {
        'size': img.size,
        'alpha': img.split()[3]
    }


with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'bg.png')) as image:
    IMAGE_LAYER_1 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'bg_chat_color_2.png')) as image:
    IMAGE_LAYER_2 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'message_clouds_out.png')) as image:
    IMAGE_LAYER_3 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'message_clouds_in.png')) as image:
    IMAGE_LAYER_4 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'prime_txt.png')) as image:
    IMAGE_LAYER_5 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'second_txt.png')) as image:
    IMAGE_LAYER_6 = {
        'img_data': list(image.getdata()),
        'alpha': list(image.split()[3].getdata()),
        'size': image.size
    }
with Image.open(os.path.join('core', 'image', 'android_theme_layers', 'shadow.png')) as image:
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


async def users_icons_v2(colors):
    painted_icons = []
    images = [
    USER_ICON_1, USER_ICON_2, USER_ICON_3, USER_ICON_4,
    USER_ICON_5, USER_ICON_6, USER_ICON_7, USER_ICON_8
    ]
    fill_start_y = 269
    fill_end_y = 343

    for image in images:
        width, _ = image['size']
        new_img = Image.new("RGBA", image['size'])
        alpha_channel = image['alpha']
            
        gradient_start_color = colors[0]
        gradient_end_color = colors[1]

        draw = ImageDraw.Draw(new_img)

        for y in range(fill_start_y, fill_end_y):
            t = (y - fill_start_y) / (fill_end_y - fill_start_y)
            r = int((1 - t) * gradient_start_color[0] + t * gradient_end_color[0])
            g = int((1 - t) * gradient_start_color[1] + t * gradient_end_color[1])
            b = int((1 - t) * gradient_start_color[2] + t * gradient_end_color[2])
            
            intermediate_color = (r, g, b)
            
            draw.line([(0, y), (width, y)], fill=intermediate_color)

        new_img.putalpha(alpha_channel)
        fill_start_y += 94
        fill_end_y += 94
        painted_icons.append(new_img)
    
    return painted_icons


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


async def create_android_preview(chat_id, photo, alfa, bg, primary_txt, secondary_txt, chat_in,
                           avatar_gradient1, avatar_gradient2, preview_bg):
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
        bg+alfa,
        chat_in+alfa,
        primary_txt,
        secondary_txt,
        avatar_gradient2
    ])

    
    assets = await set_color_v2(images, colors)
    layers.extend(i for i in assets)
    
    icons = await users_icons_v2(await hex_to_rgba_v2([avatar_gradient1, avatar_gradient2]))
    layers.extend(i for i in icons)
    
    background.paste(wallpaper, (45, 155))
    
    for layer in layers:
        background.paste(layer, (0, 0), layer)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("arial.ttf", 20)
    text_color = colors[1]
    position = (40, 1025)

    draw.text(position, PREVIEW_WATER_MARK, font=font, fill=text_color)
    
    preview = os.path.join('android', 'theme', str(chat_id), 'preview.jpg')
    
    background.save(preview)
    
    return preview
