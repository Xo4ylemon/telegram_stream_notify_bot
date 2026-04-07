import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from Handlers.start import router as start_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера (parse_mode отключен для избежания ошибок)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    """Главная функция запуска бота"""
    logger.info("Бот запускается...")

    # Регистрация хендлеров
    dp.include_router(start_router)
    logger.info("Хендлеры зарегистрированы")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())