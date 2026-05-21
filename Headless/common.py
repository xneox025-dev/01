from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

def get_main_keyboard():
    kb = [
        [KeyboardButton(text="💪 Трекер"), KeyboardButton(text="🤖 ИИ-Чат")],
        [KeyboardButton(text="📅 Календарь и Напоминания"), KeyboardButton(text="📓 Дневник")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! 👋\n"
        f"Я твой персональный ассистент. Выбери нужный раздел в меню ниже:",
        reply_markup=get_main_keyboard()
    )
