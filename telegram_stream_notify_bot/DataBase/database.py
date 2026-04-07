import sqlite3
from typing import Optional
from config import DB_PATH


class Database:
    """Класс для работы с SQLite базой данных"""

    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        """Инициализация БД - создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            with open("DataBase/migrations/init.sql", "r", encoding="utf-8") as f:
                conn.executescript(f.read())

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