import json
import time
from typing import Optional, List, Dict, Any
from .database import db


class UserDB:
    """CRUD операции для пользователей"""

    @staticmethod
    def create_user(user_id: int, ref_code: Optional[str] = None) -> Dict[str, Any]:
        """Создать нового пользователя"""
        # Генерируем уникальный реферальный код
        import random
        import string
        unique_code = f"ref_{''.join(random.choices(string.ascii_letters + string.digits, k=6))}"

        # Проверяем, не существует ли уже пользователь
        existing = db.fetch_one("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if existing:
            return UserDB.get_user(user_id)

        # Создаем пользователя
        created_at = int(time.time())
        db.execute(
            """INSERT INTO users (user_id, ref_code, created_at, extra_chats) 
               VALUES (?, ?, ?, ?)""",
            (user_id, unique_code, created_at, json.dumps([]))
        )

        # Обработка реферальной ссылки
        if ref_code and ref_code.startswith("ref_"):
            referrer = db.fetch_one("SELECT user_id FROM users WHERE ref_code = ?", (ref_code,))
            if referrer:
                referrer_id = referrer["user_id"]
                # Обновляем список приглашенных
                invited = db.fetch_one("SELECT ref_invited FROM users WHERE user_id = ?", (referrer_id,))
                if invited:
                    invited_list = json.loads(invited["ref_invited"])
                    if user_id not in invited_list:
                        invited_list.append(user_id)
                        db.execute(
                            "UPDATE users SET ref_invited = ? WHERE user_id = ?",
                            (json.dumps(invited_list), referrer_id)
                        )
                # Устанавливаем referrer для нового пользователя
                db.execute("UPDATE users SET ref_by = ? WHERE user_id = ?", (referrer_id, user_id))

        return UserDB.get_user(user_id)

    @staticmethod
    def get_user(user_id: int) -> Dict[str, Any]:
        """Получить данные пользователя"""
        user = db.fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not user:
            return {}

        # Преобразуем Row в dict и распарсим JSON поля
        user_dict = dict(user)
        user_dict["extra_chats"] = json.loads(user_dict.get("extra_chats", "[]"))
        user_dict["ref_invited"] = json.loads(user_dict.get("ref_invited", "[]"))

        # Проверяем истек ли премиум
        if user_dict.get("premium") and user_dict.get("premium_until"):
            if user_dict["premium_until"] < int(time.time()):
                user_dict["premium"] = False
                UserDB.update_user(user_id, {"premium": False, "premium_until": None})

        return user_dict

    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]) -> bool:
        """Обновить данные пользователя"""
        fields = []
        values = []
        for key, value in data.items():
            if key in ["extra_chats", "ref_invited"]:
                value = json.dumps(value)
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return False

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?"
        db.execute(query, tuple(values))
        return True

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Полностью удалить пользователя"""
        db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        return True

    @staticmethod
    def is_premium(user_id: int) -> bool:
        """Проверить, активен ли премиум"""
        user = UserDB.get_user(user_id)
        return user.get("premium", False)