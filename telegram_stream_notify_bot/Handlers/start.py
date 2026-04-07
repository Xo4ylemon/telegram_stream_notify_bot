from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from DataBase.users import UserDB
from Keyboards.main_kb import get_main_keyboard
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_ADMIN
import time

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

    # Отправляем приветственное сообщение (без Markdown)
    welcome_text = (
        "🎉 Добро пожаловать в Stream Notifications Bot!\n\n"
        "Я буду уведомлять тебя о начале стримов на Twitch и VK Live.\n\n"
        "📌 Что нужно сделать:\n"
        "1️⃣ Привязать Twitch или VK канал\n"
        "2️⃣ Выбрать основной чат для уведомлений\n"
        "3️⃣ Настроить типы уведомлений\n\n"
        "👉 Используй кнопки ниже для настройки."
    )

    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )


@router.my_chat_member()
async def on_bot_chat_member_update(event: ChatMemberUpdated):
    """Отслеживаем добавление бота в чаты"""
    chat = event.chat
    bot_id = event.bot.id

    # Проверяем, добавили ли бота в чат
    if event.new_chat_member.status in ["member", "administrator"]:
        # Сохраняем чат в БД
        from DataBase.database import db
        db.execute(
            "INSERT OR REPLACE INTO bot_chats (chat_id, chat_type, title, added_at) VALUES (?, ?, ?, ?)",
            (chat.id, chat.type, chat.title or chat.first_name or str(chat.id), int(time.time()))
        )
        print(f"✅ Бот добавлен в чат: {chat.title} ({chat.id})")

    # Проверяем, удалили ли бота из чата
    elif event.new_chat_member.status == "left" or event.new_chat_member.status == "kicked":
        from DataBase.database import db
        db.execute("DELETE FROM bot_chats WHERE chat_id = ?", (chat.id,))
        print(f"❌ Бот удален из чата: {chat.id}")