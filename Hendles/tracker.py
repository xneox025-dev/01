from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database as db

router = Router()

class TrackerStates(StatesGroup):
    waiting_for_weight = State()
    waiting_for_food = State()

def get_tracker_keyboard():
    kb = [
        [KeyboardButton(text="⚖️ Записать вес"), KeyboardButton(text="🍎 Добавить еду")],
        [KeyboardButton(text="📊 Статистика за сегодня"), KeyboardButton(text="🔙 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(F.text == "💪 Трекер")
async def open_tracker(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добро пожаловать в трекер здоровья! Выберите действие:", reply_markup=get_tracker_keyboard())

@router.message(F.text == "🔙 Главное меню")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    from handlers.common import get_main_keyboard
    await message.answer("Возвращаемся в главное меню.", reply_markup=get_main_keyboard())

@router.message(F.text == "⚖️ Записать вес")
async def ask_weight(message: Message, state: FSMContext):
    await state.set_state(TrackerStates.waiting_for_weight)
    await message.answer("Введите ваш текущий вес в кг (например, 74.5):")

@router.message(TrackerStates.waiting_for_weight)
async def save_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        db.log_weight(message.from_user.id, weight)
        await state.clear()
        await message.answer(f"Вес {weight} кг успешно записан! 👍", reply_markup=get_tracker_keyboard())
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

@router.message(F.text == "🍎 Добавить еду")
async def ask_food(message: Message, state: FSMContext):
    await state.set_state(TrackerStates.waiting_for_food)
    await message.answer("Введите калорийность и описание через пробел (например: '450 Обед в кафе'):")

@router.message(TrackerStates.waiting_for_food)
async def save_food(message: Message, state: FSMContext):
    try:
        parts = message.text.split(" ", 1)
        calories = int(parts[0])
        description = parts[1] if len(parts) > 1 else "Прием пищи"
        
        db.log_food(message.from_user.id, calories, description)
        await state.clear()
        await message.answer(f"Записано: {calories} ккал. Сверим баланс!", reply_markup=get_tracker_keyboard())
    except (ValueError, IndexError):
        await message.answer("Формат неверный. Напишите сначала число (калории), затем описание.")

@router.message(F.text == "📊 Статистика за сегодня")
async def show_stats(message: Message):
    today_cal = db.get_today_calories(message.from_user.id)
    await message.answer(f"📈 Статистика за сегодня:\nПотреблено калорий: {today_cal} ккал.")
    