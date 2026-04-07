from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from DataBase.users import UserDB  # Убрали точки
from Keyboards.main_kb import get_main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id

    # Разбираем реферальный код если есть
    ref_code = None
    if message.text and len(message.text.split()) > 1:
        ref_code = message.text.split()[1]

    # Создаем или получаем пользователя
    user = UserDB.create_user(user_id, ref_code)

    # Отправляем приветственное сообщение
    welcome_text = (
        "🎉 *Добро пожаловать в Stream Notifications Bot\\!*\n\n"
        "Я буду уведомлять тебя о начале стримов на *Twitch* и *VK Live*\\.\n\n"
        "📌 *Что нужно сделать:*\n"
        "1️⃣ Привязать Twitch или VK канал\n"
        "2️⃣ Выбрать основной чат для уведомлений\n"
        "3️⃣ Настроить типы уведомлений\n\n"
        "👉 Используй кнопки ниже для настройки\\."
    )

    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="MarkdownV2"
    )