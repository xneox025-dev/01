import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
import database as db
from handlers import common, ai_chat, tracker, schedule

async def main() -> None:
    # Инициализируем базу данных SQLite (создаем таблицы, если их нет)
    db.init_db()

    # Включаем логирование в консоль, чтобы видеть ошибки, если они появятся
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Создаем объект бота и передаем ему токен из конфигурации
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Регистрируем роутеры (подключаем логику из других файлов)
    dp.include_routers(
        common.router,
        ai_chat.router,
        tracker.router,
        schedule.router
    )

    # Запускаем длинный опрос (polling) — бот начинает слушать команды
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
