import sqlite3 as sq

from config import messages


CATALOG_DB = 'catalog.db'
USERS_DB = 'users.db'


async def start_db():
    db_catalog = sq.connect(CATALOG_DB)
    cur_catalog = db_catalog.cursor()
    
    db_users = sq.connect(USERS_DB)
    cur_users = db_users.cursor()
    
    cur_catalog.execute(
        'CREATE TABLE IF NOT EXISTS themes('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'category TEXT, '
            'preview TEXT, '
            'theme TEXT, '
            'device TEXT)'
    )
    cur_catalog.execute(
        'CREATE TABLE IF NOT EXISTS fonts('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'category TEXT, '
            'preview TEXT, '
            'font TEXT, '
            'device TEXT)'
    )
    
    cur_users.execute(
        'CREATE TABLE IF NOT EXISTS users('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id TEXT, '
            'chat_id TEXT, '
            'chat_type TEXT)'
    )
    
    db_catalog.commit()
    db_catalog.close()
    
    db_users.commit()
    db_users.close()


async def add_theme_to_catalog(category, preview, theme, device):
    db = sq.connect(CATALOG_DB)
    cur = db.cursor()
    
    query = f"INSERT INTO themes (category, preview, theme, device) VALUES (?, ?, ?, ?);"
    cur.execute(query, (category, preview, theme, device))
    db.commit()
    db.close()


async def add_user_to_db(user_id, chat_id, chat_type):
    db = sq.connect(USERS_DB)
    cur = db.cursor()
    
    get_query = f"SELECT chat_id from users;"
    get_cur = cur.execute(get_query)
    chat_ids = get_cur.fetchall()
    chat_ids = [i[0] for i in chat_ids]
    
    if str(chat_id) not in chat_ids:
        query = f"INSERT INTO users (user_id, chat_id, chat_type) VALUES (?, ?, ?);"
        cur.execute(query, (user_id, chat_id, chat_type))
        db.commit()
        db.close()


async def get_themes_from_catalog(device, category):
    db = sq.connect(CATALOG_DB)
    cur = db.cursor()
    
    query = "SELECT * FROM themes WHERE device = ? AND category = ?;"
    cur.execute(query, (str(device), category))

    result = cur.fetchall()
    result = [{'preview': i[2], 'theme': i[3]} for i in result]

    db.close()
    return result
