from pyrogram import Client
from pyrogram.raw.functions.account import UploadWallPaper
from pyrogram.raw.types import WallPaperSettings, WallPaper

from config.api_keys import API_ID, API_HASH

api_id = API_ID
api_hash = API_HASH

            
async def get_wallpaper_slug(session_name, image_path):
    async with Client(session_name, api_id, api_hash) as app:
        file = await app.save_file(path=image_path)
        wallp: WallPaper = await app.invoke(UploadWallPaper(
            file=file,
            mime_type='image/jpeg',
            settings=WallPaperSettings()
        ))
        return wallp.slug
