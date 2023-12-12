import os

from PIL import Image, ImageDraw, ImageFont


async def create_image(color_list, image_name):
    # Створення зображення з білим фоном
    image = Image.new("RGB", (720, 465), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Розмір та положення першого прямокутника
    width, height = 120, 350
    radius = 10

    rectangles = [
        {'color': color_list[0], 'position': (20, 20)},
        {'color': color_list[1], 'position': (160, 20)},
        {'color': color_list[2], 'position': (300, 20)},
        {'color': color_list[3], 'position': (440, 20)},
        {'color': color_list[4], 'position': (580, 20)}
    ]

    # Малювання інших прямокутників
    for rectangle in rectangles:
        color = rectangle['color']
        position = rectangle['position']
        x, y = position
        draw.rounded_rectangle([(x, y), (x + width, y + height)], fill=color, outline=None, width=0, radius=radius)

    # розміщення цифр
    font = ImageFont.truetype("arial.ttf", 35)

    color_position = [
        {'text': '1', 'position': (70, 300)},
        {'text': '2', 'position': (210, 300)},
        {'text': '3', 'position': (350, 300)},
        {'text': '4', 'position': (490, 300)},
        {'text': '5', 'position': (630, 300)}
    ]

    for position in color_position:
        draw.text(position['position'], position['text'], font=font, fill='white', stroke_width=3, stroke_fill='black')

    # розмішення нижніх прямокутників
    width, height = 140, 55
    radius = 10

    draw.rounded_rectangle([(20, 380), (220, 435)], fill='white', outline='grey', width=3, radius=radius)
    draw.rounded_rectangle([(240, 380), (460, 435)], fill='black', outline=None, width=0, radius=radius)
    draw.rounded_rectangle([(480, 380), (590, 435)], fill=color_list[0], outline=None, width=0, radius=radius)
    draw.rounded_rectangle([(590, 380), (700, 435)], fill=color_list[3], outline=None, width=0, radius=radius)
    draw.polygon([(553, 380), (656, 380), (623, 435), (520, 435)], fill=color_list[4])

    draw.text((70, 390), text='White', font=font, fill='black', stroke_width=1, stroke_fill='black')
    draw.text((305, 390), text='Black', font=font, fill='white', stroke_width=1, stroke_fill='white')
    draw.text((550, 390), text='Auto', font=font, fill='white', stroke_width=3, stroke_fill='black')

    path = os.path.join('gener_image', image_name)
    image.save(path)

