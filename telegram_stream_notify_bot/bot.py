import asyncio
import logging
import sys
from pathlib import Path

# Добавляем текущую папку в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# Импортируем роутеры
from Handlers.start import router as start_router
from Handlers.menu import router as menu_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота - НЕ ставим parse_mode по умолчанию
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    """Главная функция запуска бота"""
    logger.info("Бот запускается...")

    # Регистрируем все роутеры
    dp.include_router(start_router)
    dp.include_router(menu_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())