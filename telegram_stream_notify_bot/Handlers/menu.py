from aiogram import Router, F
from aiogram.types import Message
from DataBase.users import UserDB
from Keyboards.main_kb import get_main_keyboard

router = Router()


@router.message(F.text == "⚙️ Настройки бота")
async def settings_menu(message: Message):
    await message.answer("⚙️ Раздел настроек в разработке...")


@router.message(F.text == "💎 Подписка: 🔹 Обычная")
@router.message(F.text == "💎 Подписка: 💎 Премиум")
async def premium_info(message: Message):
    user_id = message.from_user.id
    is_premium = UserDB.is_premium(user_id)

    if is_premium:
        text = "💎 У вас активна Премиум подписка!"
    else:
        text = "💎 Премиум подписка - больше возможностей!"

    await message.answer(text)


@router.message(F.text.contains("Статус мониторинга"))
async def toggle_monitor(message: Message):
    user_id = message.from_user.id
    user = UserDB.get_user(user_id)
    current = user.get('monitor_active', True)
    is_premium = UserDB.is_premium(user_id)

    # Переключаем статус
    new_status = not current
    UserDB.update_user(user_id, {'monitor_active': new_status})

    # Отправляем сообщение с новой клавиатурой
    if new_status:
        status_text = "🟢 Активен"
        answer_text = "✅ Мониторинг включен"
    else:
        status_text = "🔴 Остановлен"
        answer_text = "❌ Мониторинг остановлен"

    # Обновляем клавиатуру (кнопка статуса изменится)
    await message.answer(
        answer_text,
        reply_markup=get_main_keyboard(is_premium, new_status)
    )


@router.message(F.text == "🎮 Twitch канал")
async def twitch_settings(message: Message):
    await message.answer("🎮 Настройка Twitch канала (будет добавлена позже)")


@router.message(F.text == "🎥 VK Live канал")
async def vk_settings(message: Message):
    await message.answer("🎥 Настройка VK Live канала (будет добавлена позже)")


@router.message(F.text == "📢 Основной чат")
async def main_chat_settings(message: Message):
    await message.answer("📢 Используйте /link в нужном чате для привязки")


@router.message(F.text == "➕ Дополнительные чаты")
async def extra_chats_menu(message: Message):
    await message.answer("➕ Используйте /link в нужном чате для добавления")


@router.message(F.text == "📝 Текст уведомления (шаблон)")
async def template_settings(message: Message):
    await message.answer("📝 Настройка шаблона будет доступна позже")


@router.message(F.text == "🖼 Баннер уведомления")
async def banner_settings(message: Message):
    await message.answer("🖼 Отправьте фото для баннера")


@router.message(F.text == "🔔 Уведомления")
async def notifications_menu(message: Message):
    await message.answer("🔔 Настройка типов уведомлений будет позже")


@router.message(F.text == "⏱ Кулдауны")
async def cooldowns_menu(message: Message):
    await message.answer("⏱ Настройка кулдаунов будет доступна в премиум версии")


@router.message(F.text == "👥 Реферальная система")
async def referral_info(message: Message):
    user_id = message.from_user.id
    user = UserDB.get_user(user_id)
    bot_info = await message.bot.get_me()

    text = f"👥 Ваша реферальная ссылка:\nhttps://t.me/{bot_info.username}?start={user.get('ref_code')}"
    await message.answer(text)


@router.message(F.text == "📊 Статистика")
async def show_stats(message: Message):
    user_id = message.from_user.id
    user = UserDB.get_user(user_id)

    text = (
        f"📊 Ваша статистика:\n\n"
        f"Всего уведомлений: {user.get('stats_total', 0)}\n"
        f"Twitch: {user.get('stats_twitch', 0)}\n"
        f"VK Live: {user.get('stats_vk', 0)}"
    )
    await message.answer(text)


@router.message(F.text == "📨 Тест уведомления")
async def test_notification_handler(message: Message):
    """Отправить тестовое уведомление во все чаты"""
    user_id = message.from_user.id
    user = UserDB.get_user(user_id)

    main_chat = user.get("main_chat_id")
    extra_chats = user.get("extra_chats", [])
    all_chats = [main_chat] + extra_chats if main_chat else extra_chats

    if not all_chats:
        await message.answer(
            "❌ Нет привязанных чатов.\n\n"
            "Сначала добавьте основной чат через раздел '📢 Основной чат'"
        )
        return

    # Отправляем тестовое уведомление (БЕЗ Markdown)
    success_count = 0
    failed_chats = []

    for chat_id in all_chats:
        try:
            await message.bot.send_message(
                chat_id,
                "🧪 ТЕСТОВОЕ УВЕДОМЛЕНИЕ\n\n"
                "Если вы видите это сообщение, значит бот правильно настроен и может отправлять уведомления!\n\n"
                "✅ Канал: test_channel\n"
                "🎮 Игра: Test Game\n"
                "👉 Ссылка: https://twitch.tv/example"
            )
            success_count += 1
        except Exception as e:
            failed_chats.append(f"{chat_id} ({str(e)[:50]})")

    result_text = f"✅ Тестовое уведомление отправлено в {success_count}/{len(all_chats)} чатов.\n\n"
    if failed_chats:
        result_text += f"❌ Ошибки в чатах: {', '.join(failed_chats)}\n\n"
    result_text += "Проверьте чаты, где я добавлен и есть права администратора."

    await message.answer(result_text)


@router.message(F.text == "🗑 Удалить все данные")
async def confirm_delete(message: Message):
    await message.answer("⚠️ Отправьте DELETE_ME для подтверждения")


@router.message(F.text == "🔄 Перезапустить бота")
async def restart_bot(message: Message):
    user_id = message.from_user.id
    is_premium = UserDB.is_premium(user_id)

    # Включаем мониторинг
    UserDB.update_user(user_id, {'monitor_active': True})

    await message.answer(
        "✅ Мониторинг перезапущен",
        reply_markup=get_main_keyboard(is_premium, True)
    )