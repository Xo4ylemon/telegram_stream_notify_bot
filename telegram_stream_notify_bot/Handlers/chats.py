from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.enums import ChatType
from DataBase.users import UserDB
from Keyboards.inline_kb import get_chats_keyboard, get_extra_chats_keyboard, get_link_choice_keyboard

router = Router()


# ========== ОСНОВНЫЕ МЕНЮ ==========

@router.message(F.text == "📢 Основной чат")
async def main_chat_settings(message: Message):
    """Настройка основного чата"""
    user_id = message.from_user.id
    user = UserDB.get_user(user_id)

    current_chat = user.get("main_chat_id")
    current_chat_name = "❌ Не выбран"

    if current_chat:
        try:
            chat = await message.bot.get_chat(current_chat)
            current_chat_name = chat.title or chat.first_name or str(current_chat)
        except:
            current_chat_name = f"Чат {current_chat} (бот удален)"

    text = (
        f"📢 Основной чат для уведомлений\n\n"
        f"Текущий чат: {current_chat_name}\n\n"
        f"Уведомления будут отправляться сюда.\n"
        f"Выберите способ привязки:"
    )

    await message.answer(text, reply_markup=get_chats_keyboard("main"))


@router.message(F.text == "➕ Дополнительные чаты")
async def extra_chats_settings(message: Message):
    """Настройка дополнительных чатов"""
    user_id = message.from_user.id
    user = UserDB.get_user(user_id)

    extra_chats = user.get("extra_chats", [])
    premium = user.get("premium", False)
    max_chats = 10 if premium else 3

    text = (
        f"➕ Дополнительные чаты\n\n"
        f"Добавлено: {len(extra_chats)}/{max_chats}\n"
        f"Уведомления дублируются во все чаты.\n\n"
        f"Выберите действие:"
    )

    await message.answer(text, reply_markup=get_chats_keyboard("extra"))


# ========== ВЫБОР ЧАТА ИЗ СПИСКА (СПОСОБ А) ==========

@router.callback_query(F.data == "chat_select_main")
async def chat_select_main(callback: CallbackQuery):
    """Выбор основного чата из списка"""
    user_id = callback.from_user.id

    # Сохраняем тип чата во временные данные
    if not hasattr(callback.bot, 'temp_data'):
        callback.bot.temp_data = {}
    callback.bot.temp_data[f"select_chat_type_{user_id}"] = "main"

    await callback.message.edit_text(
        "📋 Выбор основного чата\n\n"
        "Отправьте ID чата цифрами.\n\n"
        "Как получить ID чата:\n"
        "1. Добавьте бота @userinfobot в чат\n"
        "2. Напишите /start - бот покажет ID\n"
        "3. Скопируйте число и отправьте сюда"
    )
    await callback.answer()


@router.callback_query(F.data == "chat_select_extra")
async def chat_select_extra(callback: CallbackQuery):
    """Выбор дополнительного чата из списка"""
    user_id = callback.from_user.id

    # Сохраняем тип чата во временные данные
    if not hasattr(callback.bot, 'temp_data'):
        callback.bot.temp_data = {}
    callback.bot.temp_data[f"select_chat_type_{user_id}"] = "extra"

    await callback.message.edit_text(
        "📋 Выбор дополнительного чата\n\n"
        "Отправьте ID чата цифрами.\n\n"
        "Как получить ID чата:\n"
        "1. Добавьте бота @userinfobot в чат\n"
        "2. Напишите /start - бот покажет ID\n"
        "3. Скопируйте число и отправьте сюда"
    )
    await callback.answer()


# ========== ОБРАБОТКА ВВЕДЕННОГО ID ЧАТА ==========

@router.message(F.text.isdigit())
async def process_chat_id_input(message: Message):
    """Обработка введенного ID чата"""
    user_id = message.from_user.id
    chat_id = int(message.text)

    # Проверяем, есть ли временные данные о типе чата
    if not hasattr(message.bot, 'temp_data'):
        message.bot.temp_data = {}

    chat_type = message.bot.temp_data.get(f"select_chat_type_{user_id}")
    if not chat_type:
        # Не в режиме выбора чата - игнорируем
        return

    # Очищаем временные данные
    message.bot.temp_data.pop(f"select_chat_type_{user_id}", None)

    # Проверяем, может ли бот писать в чат
    try:
        await message.bot.send_message(chat_id, "🔍 Проверка подключения к чату...")
    except Exception as e:
        await message.answer(
            f"❌ Ошибка: не могу написать в чат {chat_id}\n\nУбедитесь, что бот добавлен в чат и есть права администратора.\n\nОшибка: {e}")
        return

    user = UserDB.get_user(user_id)

    if chat_type == "main":
        # Устанавливаем основной чат
        UserDB.update_user(user_id, {"main_chat_id": chat_id})
        await message.answer(f"✅ Основной чат установлен! (ID: {chat_id})")

        # Показываем информацию о чате
        try:
            chat = await message.bot.get_chat(chat_id)
            chat_name = chat.title or chat.first_name or str(chat_id)
            await message.answer(f"📢 Название чата: {chat_name}\n\nТеперь уведомления будут отправляться сюда.")
        except:
            pass

    elif chat_type == "extra":
        # Добавляем дополнительный чат
        premium = user.get("premium", False)
        max_chats = 10 if premium else 3
        extra_chats = user.get("extra_chats", [])

        if len(extra_chats) >= max_chats:
            await message.answer(
                f"❌ Достигнут лимит дополнительных чатов ({max_chats}). Удалите ненужные или приобретите Premium.")
            return

        if chat_id in extra_chats:
            await message.answer("❌ Этот чат уже добавлен в дополнительные.")
            return

        extra_chats.append(chat_id)
        UserDB.update_user(user_id, {"extra_chats": extra_chats})
        await message.answer(
            f"✅ Чат добавлен в дополнительные! (ID: {chat_id})\n\nДобавлено чатов: {len(extra_chats)}/{max_chats}")

    # Показываем главное меню
    from Keyboards.main_kb import get_main_keyboard
    await message.answer("Возврат в главное меню", reply_markup=get_main_keyboard())


# ========== ИНСТРУКЦИЯ ДЛЯ /link (СПОСОБ Б) ==========

@router.callback_query(F.data == "chat_link_main")
async def chat_link_main_instruction(callback: CallbackQuery):
    """Инструкция для привязки основного чата через /link"""
    await callback.message.edit_text(
        "📌 Как привязать основной чат через /link\n\n"
        "1️⃣ Добавьте бота в нужный чат (группу или канал)\n"
        "2️⃣ Дайте боту права администратора\n"
        "3️⃣ Напишите в этом чате команду: /link\n"
        "4️⃣ Бот пришлёт вам в личные сообщения кнопки для выбора\n"
        "5️⃣ Нажмите «Как основной чат»\n\n"
        "❗ Важно: у бота должны быть права на отправку сообщений\n\n"
        "После этого уведомления будут отправляться в этот чат."
    )
    await callback.answer()


@router.callback_query(F.data == "chat_link_extra")
async def chat_link_extra_instruction(callback: CallbackQuery):
    """Инструкция для добавления дополнительного чата через /link"""
    await callback.message.edit_text(
        "📌 Как добавить дополнительный чат через /link\n\n"
        "1️⃣ Добавьте бота в нужный чат (группу или канал)\n"
        "2️⃣ Дайте боту права администратора\n"
        "3️⃣ Напишите в этом чате команду: /link\n"
        "4️⃣ Бот пришлёт вам в личные сообщения кнопки для выбора\n"
        "5️⃣ Нажмите «Как дополнительный чат»\n\n"
        "❗ Важно: у бота должны быть права на отправку сообщений\n\n"
        "Уведомления будут дублироваться во все дополнительные чаты."
    )
    await callback.answer()


# ========== УДАЛЕНИЕ ЧАТА ==========

@router.callback_query(F.data == "chat_remove")
async def remove_chat_start(callback: CallbackQuery):
    """Начать удаление чата"""
    user_id = callback.from_user.id
    user = UserDB.get_user(user_id)

    main_chat = user.get("main_chat_id")
    extra_chats = user.get("extra_chats", [])

    if not main_chat and not extra_chats:
        await callback.message.edit_text("❌ Нет привязанных чатов.")
        await callback.answer()
        return

    await callback.message.edit_text(
        "🗑 Выберите чат для удаления:",
        reply_markup=get_extra_chats_keyboard(user)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("chat_remove_id_"))
async def confirm_remove_chat(callback: CallbackQuery):
    """Подтверждение удаления чата"""
    parts = callback.data.split("_")
    chat_id = int(parts[3])
    user_id = callback.from_user.id
    user = UserDB.get_user(user_id)

    if user.get("main_chat_id") == chat_id:
        UserDB.update_user(user_id, {"main_chat_id": None})
        await callback.message.edit_text("✅ Основной чат удален. Добавьте новый, чтобы продолжить мониторинг.")
    elif chat_id in user.get("extra_chats", []):
        extra = user.get("extra_chats", [])
        extra.remove(chat_id)
        UserDB.update_user(user_id, {"extra_chats": extra})
        await callback.message.edit_text("✅ Чат удален из дополнительных.")
    else:
        await callback.message.edit_text("❌ Чат не найден.")

    await callback.answer()


# ========== КОМАНДА /link В ГРУППЕ ==========

@router.message(Command("link"))
async def link_chat_command(message: Message):
    """Обработка команды /link в чате - ответ в ЛС"""
    chat = message.chat
    user_id = message.from_user.id

    if chat.type == ChatType.PRIVATE:
        await message.answer(
            "❌ Команда /link работает только в групповых чатах и каналах.\n\nДобавьте бота в группу и напишите /link там.")
        return

    # Проверяем, есть ли бот в чате
    try:
        bot_member = await message.bot.get_chat_member(chat.id, message.bot.id)
        if bot_member.status not in ["administrator", "member", "creator"]:
            await message.answer("❌ Бот не найден в этом чате.")
            return
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
        return

    user = UserDB.get_user(user_id)
    premium = user.get("premium", False)
    extra_chats = user.get("extra_chats", [])
    max_chats = 10 if premium else 3
    current_extra = len(extra_chats)

    limit_text = ""
    if current_extra >= max_chats:
        limit_text = f"\n\n⚠️ Достигнут лимит дополнительных чатов ({max_chats})."

    chat_title = chat.title or str(chat.id)

    await message.answer(f"✅ Запрос принят! Проверьте личные сообщения от бота.")

    try:
        await message.bot.send_message(
            user_id,
            f"📌 Привязка чата\n\n"
            f"Чат: {chat_title}\n"
            f"ID: {chat.id}\n\n"
            f"📊 У вас уже добавлено: {current_extra}/{max_chats} дополнительных чатов{limit_text}\n\n"
            f"Куда добавить этот чат?",
            reply_markup=get_link_choice_keyboard(chat.id, user_id)
        )
    except Exception as e:
        await message.answer(
            f"❌ Не могу отправить сообщение в ЛС. Пожалуйста, начните диалог с ботом: @{message.bot.username}\n\n"
            f"Чат: {chat_title}\n\n"
            f"Куда добавить?",
            reply_markup=get_link_choice_keyboard(chat.id, user_id)
        )


# ========== ОБРАБОТЧИКИ ВЫБОРА ИЗ /link ==========

@router.callback_query(F.data.startswith("link_main_"))
async def link_set_main(callback: CallbackQuery):
    """Установить чат как основной через /link"""
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("❌ Ошибка", show_alert=True)
        return

    chat_id = int(parts[2])
    user_id = int(parts[3]) if len(parts) > 3 else callback.from_user.id

    if callback.from_user.id != user_id:
        await callback.answer("❌ Эта кнопка не для вас", show_alert=True)
        return

    UserDB.update_user(user_id, {"main_chat_id": chat_id})

    await callback.message.edit_text(
        f"✅ Основной чат установлен!\n\n"
        f"Чат ID: {chat_id}\n"
        f"Теперь уведомления будут отправляться сюда."
    )
    await callback.answer()


@router.callback_query(F.data.startswith("link_extra_"))
async def link_set_extra(callback: CallbackQuery):
    """Добавить чат как дополнительный через /link"""
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("❌ Ошибка", show_alert=True)
        return

    chat_id = int(parts[2])
    user_id = int(parts[3]) if len(parts) > 3 else callback.from_user.id

    if callback.from_user.id != user_id:
        await callback.answer("❌ Эта кнопка не для вас", show_alert=True)
        return

    user = UserDB.get_user(user_id)
    premium = user.get("premium", False)
    max_chats = 10 if premium else 3
    extra_chats = user.get("extra_chats", [])

    if len(extra_chats) >= max_chats:
        await callback.message.edit_text(f"❌ Достигнут лимит дополнительных чатов ({max_chats}).")
        await callback.answer()
        return

    if chat_id in extra_chats:
        await callback.message.edit_text(f"❌ Чат {chat_id} уже добавлен.")
        await callback.answer()
        return

    extra_chats.append(chat_id)
    UserDB.update_user(user_id, {"extra_chats": extra_chats})

    await callback.message.edit_text(
        f"✅ Чат добавлен в дополнительные!\n\n"
        f"Чат ID: {chat_id}\n"
        f"Добавлено чатов: {len(extra_chats)}/{max_chats}"
    )
    await callback.answer()


# ========== НАЗАД В ГЛАВНОЕ МЕНЮ ==========

@router.callback_query(F.data == "nav_main")
async def back_to_main(callback: CallbackQuery):
    """Вернуться в главное меню"""
    from Keyboards.main_kb import get_main_keyboard
    await callback.message.delete()
    await callback.message.answer("Главное меню:", reply_markup=get_main_keyboard())
    await callback.answer()