# import os
# import zipfile
# from datetime import datetime
# import subprocess


# from aiogram.types import Message, FSInputFile
# from sqlalchemy.ext.asyncio import AsyncSession

# from config import messages


# async def get_backup(message: Message):
#     await message.delete()
#     command = 'pg_dump -U bot_admin -h localhost -d theme_bot -W > backup.sql'

#     subprocess.run(command, shell=True, input='admin', text=True)
    
    
#     with zipfile.ZipFile('BACKUPS_DB.zip', 'w') as zipf:
#         zipf.write('backup.sql')
    
#     await message.answer_document(
#         document=FSInputFile('BACKUPS_DB.zip'),
#         caption=f'{messages.MESSAGE_BACKUP}{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
#     )
    
#     os.remove('BACKUPS_DB.zip')
#     os.remove('backup.sql')
    
    
