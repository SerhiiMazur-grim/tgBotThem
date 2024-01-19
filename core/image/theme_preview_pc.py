import os
from PIL import Image, ImageDraw, ImageFont

from config.messages import PREVIEW_WATER_MARK
from core.utils import hex_to_rgba_v2


async def crop_wallpaper(wallpaper_path):
    with Image.open(wallpaper_path) as img:
        width, height = img.size
        
        if width > height:
            top_x = width//2 - height//2
            top_y = 0
            bot_x = width//2 + height//2
            bot_y = height
            
        else:
            top_x = 0
            top_y = height//2 - width//2
            bot_x = width
            bot_y = height//2 + width//2

        cropped_img = img.crop((top_x, top_y, bot_x, bot_y))
    wallpaper = cropped_img.resize((535, 555))
    
    return wallpaper


async def users_icons_v2(colors):
    painted_icons = []
    images = [
    'user_icon_1.png', 'user_icon_2.png', 'user_icon_3.png', 'user_icon_4.png',
    'user_icon_5.png', 'user_icon_6.png', 'user_icon_7.png',
    ]
    fill_start_y = 335
    fill_end_y = 398

    for image in images:
        with Image.open(os.path.join('core', 'image', 'pc_theme_layers', image)) as img:
            width, _ = img.size
            new_img = Image.new("RGBA", img.size)
            alpha_channel = img.split()[3]
            
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
        fill_start_y += 80
        fill_end_y += 80
        painted_icons.append(new_img)
        
    return painted_icons


async def set_color_v2(images, colors):
    layers = []
    for image, color in zip(images, colors):
        with Image.open(image) as img:

            img_data = list(img.getdata())
            alpha_channel = list(img.split()[3].getdata())

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

        new_img = Image.new("RGBA", img.size)
        new_img.putdata([tuple(p) for p in new_img_data])
        layers.append(new_img)

    return layers


async def create_pc_preview(chat_id, photo, img_bg_color, chat_bg, clouds_in_color, 
                              secondary_txt_color, prime_txt_color, alfa,):
    background = Image.new('RGB', (1088, 1088), 'white')

    layers = []
    wallpaper = await crop_wallpaper(photo)
    images = [
        os.path.join('core', 'image', 'pc_theme_layers', 'img_bg.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'chat_bg.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'side_bar.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'selected_chat.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'clouds_in.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'clouds_out.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'prime_txt.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'secondary_txt.png'),
        os.path.join('core', 'image', 'pc_theme_layers', 'shadows.png'),
    ]
    
    colors = await hex_to_rgba_v2([
        img_bg_color,
        chat_bg,
        clouds_in_color,
        secondary_txt_color,
        clouds_in_color+alfa,
        chat_bg+alfa,
        prime_txt_color,
        secondary_txt_color,
        secondary_txt_color,
    ])

    
    assets = await set_color_v2(images, colors)
    layers.extend(i for i in assets)
    
    icons = await users_icons_v2(await hex_to_rgba_v2([chat_bg, secondary_txt_color]))
    layers.extend(i for i in icons)
    
    background.paste(wallpaper, (511, 304))
    
    for layer in layers:
        background.paste(layer, (0, 0), layer)
    
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("arial.ttf", 20)
    text_color = colors[1]
    position = (40, 1025)

    draw.text(position, PREVIEW_WATER_MARK, font=font, fill=text_color)
    
    preview = os.path.join('desktop', 'theme', str(chat_id), 'preview.jpg')
    
    background.save(preview)
    
    return preview
