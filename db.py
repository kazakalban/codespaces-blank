import sqlite3


__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('anketa.db')


def init_db(force: bool = False):
    """ Проверить что нужные таблицы существют, иначе создать их
        Важно: миграция на такие табличы вы должны производить самостоятельно!
        :param force: явно пересоздать все таблицы
    """
    conn = get_connection()

    c = conn.cursor()
    
    if force:
        c.execute('DROP TABLE IF EXISTS find_number_bot_user_data')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS find_number_bot_user_data (
            user_id INTEGER PRIMARY KEY,
            is_bot BOOLEAN NOT NULL,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            type TEXT NOT NULL
        )
    ''')

    # Сохранить изменения
    conn.commit()


def add_user(user_id: int, is_bot: bool, first_name:str, last_name:str, username:str, type:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO find_number_bot_user_data (user_id, is_bot, first_name, last_name, username) VALUES (?, ?, ?, ?, ?)', (user_id, is_bot, first_name, last_name, username))
    conn.commit()

if __name__ == '__main__':
    init_db()

    add_user(user_id=777, is_bot=False, username='kass', first_name='Kassym', last_name='Sauyt', type=False)