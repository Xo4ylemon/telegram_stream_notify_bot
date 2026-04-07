# работа с премиум кодами
import time
import random
import string
from typing import Optional, Dict, Any, List
from .database import db


class PremiumCodeDB:
    """CRUD операции для премиум кодов"""

    @staticmethod
    def generate_code(days: int, length: int = 12) -> str:
        """Сгенерировать уникальный код"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def create_codes(count: int, days: int) -> List[str]:
        """Создать несколько кодов"""
        codes = []
        created_at = int(time.time())

        for _ in range(count):
            code = PremiumCodeDB.generate_code(days)
            db.execute(
                "INSERT INTO premium_codes (code, days, created_at) VALUES (?, ?, ?)",
                (code, days, created_at)
            )
            codes.append(code)

        return codes

    @staticmethod
    def use_code(code: str, user_id: int) -> Dict[str, Any]:
        """Активировать код для пользователя"""
        code_data = db.fetch_one(
            "SELECT * FROM premium_codes WHERE code = ? AND used = 0",
            (code,)
        )

        if not code_data:
            return {"success": False, "error": "Код не найден или уже использован"}

        # Активируем код
        used_at = int(time.time())
        db.execute(
            "UPDATE premium_codes SET used = 1, used_by = ?, used_at = ? WHERE code = ?",
            (user_id, used_at, code)
        )

        # Выдаём премиум пользователю
        from .users import UserDB
        premium_until = used_at + (code_data["days"] * 86400)
        UserDB.update_user(user_id, {
            "premium": True,
            "premium_until": premium_until
        })

        return {
            "success": True,
            "days": code_data["days"],
            "premium_until": premium_until
        }

    @staticmethod
    def get_unused_codes() -> List[Dict[str, Any]]:
        """Получить все неиспользованные коды"""
        codes = db.fetch_all("SELECT code, days, created_at FROM premium_codes WHERE used = 0")
        return [dict(code) for code in codes]

    @staticmethod
    def get_code_info(code: str) -> Optional[Dict[str, Any]]:
        """Получить информацию о коде"""
        result = db.fetch_one("SELECT * FROM premium_codes WHERE code = ?", (code,))
        return dict(result) if result else None