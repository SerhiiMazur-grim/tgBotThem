from datetime import datetime, timedelta, time
import os
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message


clean_time = None


class CleanupMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if clean_time:
            current_time = datetime.now()
            time_difference = current_time - clean_time
            
            if time_difference.total_seconds() >= 0:
                await check_and_delete_files()
            
        return await handler(event, data)
    

async def check_and_delete_files():
    global clean_time
    download_photo_folder = 'download_photo'
    gener_image_folder = 'gener_image'

    # Перевіряємо наявність папок
    if not os.path.exists(download_photo_folder) or not os.path.exists(gener_image_folder):
        return

    # Ініціалізуємо список для зберігання шляхів до файлів, які потрібно видалити
    files_to_delete = []

    # Перевіряємо файли в папці download_photo
    for filename in os.listdir(download_photo_folder):
        file_path = os.path.join(download_photo_folder, filename)
        if os.path.isfile(file_path):
            files_to_delete.append(file_path)

    # Перевіряємо файли в папці gener_image
    for filename in os.listdir(gener_image_folder):
        file_path = os.path.join(gener_image_folder, filename)
        if os.path.isfile(file_path):
            files_to_delete.append(file_path)

    # Перевіряємо, чи є файли для видалення
    if files_to_delete:
        # Видаляємо файли зі списку
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {str(e)}")
        print('Folders cleaned.')
    
    current_datetime = datetime.now()
    # Додаємо один день до дати
    new_date = current_datetime + timedelta(days=1)
    # Встановлюємо час на 3:00 години ночі
    new_time = time(3, 0, 0)
    # Поєднуємо нову дату та час в один об'єкт datetime
    clean_time = datetime.combine(new_date, new_time)
    
