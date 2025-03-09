import sqlite3
import os


# Определяем путь к базе данных внутри db_lession иначе anketa.db создается в корне
DB_PATH = os.path.join(os.path.dirname(__file__), "anketa.db")


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
    try:
        conn = sqlite3.connect(DB_PATH)  # Используем полный путь
        print("Подключение успешно:", DB_PATH)  # Отладочный вывод

        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                is_bot BOOLEAN NOT NULL,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                type TEXT NOT NULL
            )
        ''')

        conn.commit()

        print("База данных и таблица созданы!")

    except sqlite3.Error as e:
        print("Ошибка при подключении к базе данных:", e)

    # Сохранить изменения
    conn.commit()


def add_user(user_id: int, is_bot: bool, first_name:str, last_name:str, username:str, type:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO find_number_bot_user_data (user_id, is_bot, first_name, last_name, username) VALUES (?, ?, ?, ?, ?)', (user_id, is_bot, first_name, last_name, username))
    conn.commit()

if __name__ == '__main__':
    init_db()

    add_user(user_id=777, is_bot=False, username='kass')