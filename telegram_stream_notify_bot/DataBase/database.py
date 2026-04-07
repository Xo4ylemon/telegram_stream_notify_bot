import sqlite3
import os
from typing import Optional
from config import DB_PATH


class Database:
    """Класс для работы с SQLite базой данных"""

    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        """Инициализация БД - создание таблиц"""
        # Создаем директорию для БД если её нет
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Проверяем, существует ли файл init.sql
        init_sql_path = os.path.join(os.path.dirname(__file__), "migrations", "init.sql")

        with sqlite3.connect(self.db_path) as conn:
            if os.path.exists(init_sql_path):
                with open(init_sql_path, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                    conn.executescript(sql_script)
                    print("Database initialized successfully")
            else:
                print(f"Warning: init.sql not found at {init_sql_path}")
                # Создаем таблицы вручную, если файла нет
                self._create_tables_manually(conn)

    def _create_tables_manually(self, conn):
        """Создать таблицы вручную (если нет init.sql)"""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                premium BOOLEAN DEFAULT 0,
                premium_until INTEGER,
                twitch_login TEXT,
                twitch_user_id TEXT,
                twitch_access_token TEXT,
                twitch_refresh_token TEXT,
                vk_user_id TEXT,
                vk_access_token TEXT,
                main_chat_id INTEGER,
                extra_chats TEXT DEFAULT '[]',
                message_template TEXT DEFAULT '✨ {channel} начал стрим на {platform}!\n🎮 {title}\n👉 {url}',
                banner_file_id TEXT,
                monitor_active BOOLEAN DEFAULT 1,
                notif_start BOOLEAN DEFAULT 1,
                notif_end BOOLEAN DEFAULT 0,
                notif_title BOOLEAN DEFAULT 0,
                notif_category BOOLEAN DEFAULT 0,
                cooldown_start INTEGER DEFAULT 0,
                cooldown_end INTEGER DEFAULT 0,
                cooldown_title INTEGER DEFAULT 60,
                cooldown_category INTEGER DEFAULT 60,
                last_notified_start INTEGER,
                last_notified_end INTEGER,
                last_notified_title INTEGER,
                last_notified_category INTEGER,
                stats_total INTEGER DEFAULT 0,
                stats_twitch INTEGER DEFAULT 0,
                stats_vk INTEGER DEFAULT 0,
                last_stream_platform TEXT,
                last_stream_title TEXT,
                last_stream_timestamp INTEGER,
                ref_code TEXT UNIQUE,
                ref_invited TEXT DEFAULT '[]',
                ref_by INTEGER,
                created_at INTEGER
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS premium_codes (
                code TEXT PRIMARY KEY,
                days INTEGER,
                used BOOLEAN DEFAULT 0,
                used_by INTEGER,
                used_at INTEGER,
                created_at INTEGER
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS notification_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                platform TEXT,
                event_type TEXT,
                sent_at INTEGER
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_ref_code ON users(ref_code)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_main_chat ON users(main_chat_id)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_notification_logs_user ON notification_logs(user_id)
        """)

        conn.commit()
        print("Tables created manually")

    def get_connection(self):
        """Получить соединение с БД"""
        return sqlite3.connect(self.db_path)

    def execute(self, query: str, params: tuple = ()):
        """Выполнить запрос"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetch_one(self, query: str, params: tuple = ()):
        """Получить одну запись"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()):
        """Получить все записи"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()


# Синглтон
db = Database()