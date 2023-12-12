import cv2
import numpy as np


async def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)


async def image_color_picker(analize_image):

    img = cv2.imread(analize_image)
    height, width, _ = np.shape(img)

    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    number_clusters = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)

    rgb_values = []

    for index, row in enumerate(centers):
        bar, rgb = await create_bar(200, 200, row)
        hex_value = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        rgb_values.append(hex_value)

    # Сортувати список rgb_values за кількістю входжень кольору на зображенні
    counts = np.bincount(labels.flatten())  # Порахувати кількість входжень кожного кластера
    sorted_indices = np.argsort(counts)[::-1]  # Отримати індекси в порядку спадання
    rgb_values_sorted = [rgb_values[i] for i in sorted_indices]

    return rgb_values_sorted
