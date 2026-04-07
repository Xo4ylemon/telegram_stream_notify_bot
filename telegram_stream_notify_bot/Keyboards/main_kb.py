from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard(is_premium: bool = False, monitor_active: bool = True) -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    monitor_status = "🟢 Активен" if monitor_active else "🔴 Остановлен"
    premium_status = "💎 Премиум" if is_premium else "🔹 Обычная"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚙️ Настройки бота")],
            [KeyboardButton(text=f"💎 Подписка: {premium_status}")],
            [KeyboardButton(text=f"📊 Статус мониторинга: {monitor_status}")],
            [KeyboardButton(text="🎮 Twitch канал"), KeyboardButton(text="🎥 VK Live канал")],
            [KeyboardButton(text="📢 Основной чат"), KeyboardButton(text="➕ Дополнительные чаты")],
            [KeyboardButton(text="📝 Текст уведомления (шаблон)")],
            [KeyboardButton(text="🖼 Баннер уведомления")],
            [KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="⏱ Кулдауны"), KeyboardButton(text="👥 Реферальная система")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📨 Тест уведомления")],
            [KeyboardButton(text="🗑 Удалить все данные"), KeyboardButton(text="🔄 Перезапустить бота")]
        ],
        resize_keyboard=True
    )
    return keyboard