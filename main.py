import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from core.base_utils import get_bot_token, get_admins_ids, get_google_api_client
from utils.google_tables import get_worksheet
from utils.setup import setup_bot_commands
from handlers import commands, messages, callbacks

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Настройка переменных
bot_token = get_bot_token()
admins = get_admins_ids()
google_api = get_google_api_client()

# Настройка бота
bot = Bot(
    token=bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())


# === Запуск бота ===
async def main():
    # Настройка кнопки меню
    await setup_bot_commands(bot)

    # Инициализация Google Sheets
    try:
        ws = await get_worksheet()
        logging.info(f"Успешное подключение к Google Sheets. Рабочий лист: {ws.title}")
    except Exception as e:
        logging.error(f"Ошибка подключения к Google Sheets: {e}")
        raise

    # Регистрируем зависимость
    dp["worksheet"] = ws

    dp.startup.register(on_startup)

    dp.include_router(commands.router)
    dp.include_router(messages.router)
    dp.include_router(callbacks.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def on_startup():
    print("Бот запущен")


if __name__ == "__main__":
    asyncio.run(main())