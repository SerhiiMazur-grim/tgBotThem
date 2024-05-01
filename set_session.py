import asyncio
from core.wallpaper_slug import get_wallpaper_slug


img_path = 'q.jpg'
SESSIONS = ["my_account", "my_account_2", "my_account_3", "my_account_4", "my_account_5"]


async def main():
    for s in SESSIONS:
        print(s)
        slug = await get_wallpaper_slug(s, img_path)
        print(slug, '\n')
    
asyncio.run(main())