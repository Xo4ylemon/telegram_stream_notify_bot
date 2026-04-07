import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
# УБИРАЕМ parse_mode по умолчанию
bot = Bot(token=BOT_TOKEN)  # Убрали parse_mode="MarkdownV2"
dp = Dispatcher()


async def main():
    """Главная функция запуска бота"""
    logger.info("Бот запускается...")

    # Импортируем роутеры здесь, чтобы избежать циклических импортов
    from Handlers import start, menu, chats

    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(chats.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())