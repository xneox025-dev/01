from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import config
from anthropic import AsyncAnthropic

router = Router()
anthropic_client = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)

class ChatStates(StatesGroup):
    talking_to_ai = State()

@router.message(F.text == "🤖 ИИ-Чат")
async def start_chat(message: Message, state: FSMContext):
    await state.set_state(ChatStates.talking_to_ai)
    await message.answer("Режим ИИ-Чата активирован! 🧠 Напиши мне что-нибудь. Для выхода из чата напиши 'выход'.")

@router.message(ChatStates.talking_to_ai)
async def chat_with_claude(message: Message, state: FSMContext):
    if message.text.lower() == "выход":
        await state.clear()
        from handlers.common import get_main_keyboard
        await message.answer("Вышли из режима ИИ-чата.", reply_markup=get_main_keyboard())
        return

    waiting_msg = await message.answer("Думаю...")
    
    try:
        response = await anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": message.text}]
        )
        await waiting_msg.delete()
        await message.answer(response.content[0].text)
    except Exception as e:
        await waiting_msg.edit_text(f"Произошла ошибка при обращении к Claude: {e}")
        