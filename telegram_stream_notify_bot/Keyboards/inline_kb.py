from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DataBase.users import UserDB


def get_chats_keyboard(action: str) -> InlineKeyboardMarkup:
    """Клавиатура для управления чатами"""
    if action == "main":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Выбрать из моих чатов", callback_data="chat_select_main")],
            [InlineKeyboardButton(text="💬 Использовать /link в чате", callback_data="chat_link_main")],
            [InlineKeyboardButton(text="🗑 Удалить чат", callback_data="chat_remove")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="nav_main")]
        ])

    elif action == "extra":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Выбрать из моих чатов", callback_data="chat_select_extra")],
            [InlineKeyboardButton(text="💬 Использовать /link в чате", callback_data="chat_link_extra")],
            [InlineKeyboardButton(text="🗑 Удалить чат", callback_data="chat_remove")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="nav_main")]
        ])

    elif action.startswith("add_"):
        chat_type = action.split("_")[1]  # main or extra
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Выбрать из моих чатов", callback_data=f"chat_select_{chat_type}")],
            [InlineKeyboardButton(text="💬 Использовать /link в чате", callback_data=f"chat_link_{chat_type}")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data=f"nav_{chat_type}_chats")]
        ])

    elif action == "cancel":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="nav_main")]
        ])

    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="nav_main")]])


def get_extra_chats_keyboard(user: dict) -> InlineKeyboardMarkup:
    """Клавиатура со списком чатов для удаления"""
    buttons = []

    main_chat = user.get("main_chat_id")
    if main_chat:
        buttons.append([InlineKeyboardButton(
            text=f"📢 Основной чат ({main_chat})",
            callback_data=f"chat_remove_id_{main_chat}"
        )])

    for chat_id in user.get("extra_chats", []):
        buttons.append([InlineKeyboardButton(
            text=f"➕ Доп. чат ({chat_id})",
            callback_data=f"chat_remove_id_{chat_id}"
        )])

    buttons.append([InlineKeyboardButton(text="⬅ Назад", callback_data="nav_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_link_choice_keyboard(chat_id: int, user_id: int) -> InlineKeyboardMarkup:
    """Клавиатура выбора типа чата при /link"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Как основной чат", callback_data=f"link_main_{chat_id}_{user_id}")],
        [InlineKeyboardButton(text="➕ Как дополнительный чат", callback_data=f"link_extra_{chat_id}_{user_id}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="nav_main")]
    ])

