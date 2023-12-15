import sqlite3 as sq

from config import messages


db = sq.connect('catalog.db')
cur = db.cursor()


async def start_db():
    cur.execute(
        'CREATE TABLE IF NOT EXISTS themes('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'category TEXT, '
            'preview TEXT, '
            'theme TEXT, '
            'device TEXT)'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS fonts('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'category TEXT, '
            'preview TEXT, '
            'font TEXT, '
            'device TEXT)'
    )
    db.commit()


async def add_theme_to_catalog(category, preview, theme, device):
    query = f"INSERT INTO themes (category, preview, theme, device) VALUES (?, ?, ?, ?);"
    cur.execute(query, (category, preview, theme, device))
    db.commit()
