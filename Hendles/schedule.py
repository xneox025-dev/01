from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📅 Календарь и Напоминания")
async def calendar_stub(message: Message):
    await message.answer(
        "📅 Модуль календаря готов к интеграции Google Calendar API.\n\n"
        "Для полноценной синхронизации требуется настроить сервисный аккаунт в Google Cloud Console "
        "и прописать `GOOGLE_REFRESH_TOKEN` в настройках сервера."
    )

@router.message(F.text == "📓 Дневник")
async def diary_stub(message: Message):
    await message.answer("📓 Раздел Дневника. Здесь можно фиксировать свои мысли за день. (В разработке)")
