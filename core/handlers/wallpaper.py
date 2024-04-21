import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from config import messages
from core.states import WallpState
from core.keyboards.inline_keybords import abort_create_wallpaper_ikb
from core.keyboards.reply_keybords import user_keyboard
from ios.iphone_theme import create_iphone_wallpaper
from core.handlers.basic import command_start


async def start_create_wallpaper(message: Message, state: FSMContext):
    my_message_1 = await message.answer(text=messages.MESSAGE_FILLER,
                         reply_markup=ReplyKeyboardRemove())
    my_message_2 = await message.answer(text=messages.MESSAGE_WALLP_START,
                         reply_markup=abort_create_wallpaper_ikb())
    await state.set_state(WallpState.photo)
    await state.set_data({'message_1': my_message_1,
                          'message_2': my_message_2})


async def create_wallpaper(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    if message.text == '/start':
        await command_start(message, bot, state, session)
        return None
    
    if not message.photo:
        return message.answer(text=messages.NOT_IMAGE)
    
    data = await state.get_data()
    my_message_1 = data.get('message_1')
    my_message_2 = data.get('message_2')
    wait_message = await message.answer(text=messages.WAIT_MESSAGE)
    user_id = message.from_user.id
    user_id = str(user_id)
    photo_id = message.photo[-1].file_id
    photo_data = await bot.get_file(photo_id)
    file_name = photo_data.file_path.split('/')[-1]
    user_folder = os.path.join('wallpaper', user_id)
    
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        
    download_to = os.path.join('wallpaper', user_id, file_name)
    await bot.download_file(file_path=photo_data.file_path,
                            destination=download_to)
    try:
        wallpaper = await create_iphone_wallpaper(download_to)
    except:
        await wait_message.delete()
        return message.answer(text=messages.MESSAGE_WALLPAPER_SOME_ERROR)
        
    await wait_message.delete()
    await my_message_1.delete()
    await my_message_2.delete()
    
    await message.answer(text=messages.wallpaper_message(wallpaper),
                                 reply_markup=user_keyboard(user_id),
                                 parse_mode=ParseMode.HTML)
    os.remove(download_to)
    await state.clear()
    
    
async def group_create_wallpaper(message: Message, bot: Bot):
    wait_message = await message.answer(text=messages.WAIT_MESSAGE)
    user_id = message.from_user.id
    user_id = str(user_id)
    photo_id = message.photo[-1].file_id
    photo_data = await bot.get_file(photo_id)
    file_name = photo_data.file_path.split('/')[-1]
    user_folder = os.path.join('wallpaper', user_id)
    
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        
    download_to = os.path.join('wallpaper', user_id, file_name)
    await bot.download_file(file_path=photo_data.file_path,
                            destination=download_to)
    try:
        wallpaper = await create_iphone_wallpaper(download_to)
    except:
        await wait_message.delete()
        return message.answer(text=messages.MESSAGE_WALLPAPER_SOME_ERROR)
        
    await wait_message.delete()
    
    await message.answer(text=messages.wallpaper_message(wallpaper),
                                #  reply_markup=user_keyboard(user_id),
                                 parse_mode=ParseMode.HTML)
    os.remove(download_to)

    
async def abort_create_wallpaper(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.delete()
    current_state = await state.get_state()
        
    if current_state is not None:
        data = await state.get_data()
        await state.clear()
        message_1 = data.get('message_1')
        await message_1.delete()
        
    
    await call.message.answer(text=messages.MESSAGE_ON_BACK,
                              reply_markup=user_keyboard(user_id))
