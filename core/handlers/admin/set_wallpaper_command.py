import os
import logging

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.methods import TelegramMethod
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from core.keyboards.inline_keybords import abort_set_wallpaper_ikb
from config import messages
from core.states import SetWallpaperState


logger = logging.getLogger(__name__)


async def insert_wallpaper(theme_path, image_path):
    color_data = []
    with open(image_path, 'rb') as f:
        binary_image = f.read()
        
    with open(theme_path, 'rb') as f:
        theme_data = f.readlines()
        for row in theme_data:
            decode_row = row.decode()
            if decode_row.startswith('WPS') or decode_row.startswith('WLS'):
                break
            else:
                color_data.append(row)
            
    with open(theme_path, 'wb') as f:
        for row in color_data:
            f.write(row)
        f.write('\nWPS\n'.encode('utf-8'))
        f.write(binary_image)
        f.write('\nWPE'.encode('utf-8'))
    
    return theme_path


async def start_set_wallpaper(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.set_state(SetWallpaperState.theme_path)
    await message.answer(text=messages.MESSAGE_SEND_ANDROID_THEME_FILE,
                         reply_markup=abort_set_wallpaper_ikb())
    

async def get_android_theme_file(message: Message, bot: Bot, state: FSMContext) -> TelegramMethod:
    file = message.document
    if file:
        if file.file_name.split('.')[-1] == 'attheme':
            get_file = await bot.get_file(file.file_id)
            src_file_path = os.path.join('src', file.file_name)
            await bot.download_file(get_file.file_path, src_file_path)
            await state.update_data(theme_path=src_file_path)
            await state.set_state(SetWallpaperState.image_path)
            
            return message.answer(text=messages.MESSAGE_SEND_WALLPAPER,
                                  reply_markup=abort_set_wallpaper_ikb())
        
    return message.answer(text=messages.ERROR_MESSAGE_SEND_ANDROID_THEME_FILE,
                            reply_markup=abort_set_wallpaper_ikb())


async def get_android_theme_wallpaper(message: Message, bot: Bot, state: FSMContext) -> None | TelegramMethod:
    photo = message.photo
    if photo:
        data = await state.get_data()
        await state.clear()
        src_theme_path = data['theme_path']
        photo = photo[-1]
        get_photo = await bot.get_file(photo.file_id)
        photo_name = get_photo.file_path.split('/')[-1]
        src_photo_path = os.path.join('src', photo_name)
        await bot.download_file(get_photo.file_path, src_photo_path)
        try:
            theme = await insert_wallpaper(src_theme_path, src_photo_path)
            await message.answer_document(document=FSInputFile(path=theme))
            os.remove(theme)
            os.remove(src_photo_path)
            return
            
        except Exception as e:
            logger.exception(e)
            return message.answer(text=messages.ERROR_MESSAGE_INSERT_WALLPAPER)
        
    
    await message.answer(text=messages.ERROR_MESSAGE_SEND_WALLPAPER,
                            reply_markup=abort_set_wallpaper_ikb())


async def abort_insert_wallaper(callback_query: CallbackQuery, state: FSMContext) -> TelegramMethod:
    await callback_query.message.delete()
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    return callback_query.message.answer(text=messages.ABORT_INSERT_WALLPAPER)
