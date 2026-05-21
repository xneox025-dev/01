from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from curl_cffi import requests

router = Router()

class ChatStates(StatesGroup):
    talking_to_ai = State()

@router.message(F.text == "🤖 ИИ-Чат")
async def start_chat(message: Message, state: FSMContext):
    await state.set_state(ChatStates.talking_to_ai)
    await message.answer("Режим бесплатного ИИ-Чата активирован! 🧠 Напиши мне что-нибудь. Для выхода напиши 'выход'.")

@router.message(ChatStates.talking_to_ai)
async def chat_with_free_ai(message: Message, state: FSMContext):
    if message.text.lower() == "выход":
        await state.clear()
        from handlers.common import get_main_keyboard
        await message.answer("Вышли из режима ИИ-чата.", reply_markup=get_main_keyboard())
        return

    waiting_msg = await message.answer("Думаю...")
    
    try:
        # Используем бесплатное API без ключей (на базе провайдера обратного прокси)
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message.text}],
            "stream": False
        }
        
        # Отправляем запрос на публичный бесплатный ИИ-эндпоинт
        response = requests.post(
            "https://free.churchless.tech/v1/chat/completions", # Стабильный бесплатный прокси-сервер ИИ
            json=payload, 
            timeout=30
        )
        
        await waiting_msg.delete()
        
        if response.status_code == 200:
            ai_text = response.json()['choices'][0]['message']['content']
            await message.answer(ai_text)
        else:
            await message.answer("Временный сбой бесплатного ИИ. Попробуй еще раз через минуту.")
            
    except Exception as e:
        await waiting_msg.delete()
        await message.answer("Не удалось связаться с бесплатным ИИ. Но трекеры работают!")
