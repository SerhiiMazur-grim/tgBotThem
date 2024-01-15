import os
import zipfile
from datetime import datetime
from aiogram.types import Message, FSInputFile

from config import messages


async def get_backup(message: Message):
    await message.delete()
    
    with zipfile.ZipFile('BACKUPS_DB.zip', 'w') as zipf:
        zipf.write('catalog.db')
        zipf.write('users.db')
        zipf.write('POST_DATA.json')
        zipf.write('SEND_POST.json')
    
    await message.answer_document(
        document=FSInputFile('BACKUPS_DB.zip'),
        caption=f'{messages.MESSAGE_BACKUP}{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
    )
    
    os.remove('BACKUPS_DB.zip')
    
    
