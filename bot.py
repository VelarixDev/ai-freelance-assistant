import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN_FILE = "token.txt"
LLM_BASE_URL = "http://127.0.0.1:1234/v1"
LLM_API_KEY = "local"
SYSTEM_PROMPT = (
    "You are a dedicated and practical Python developer named VelarixDev. "
    "Write a direct, professional proposal for the following freelance job description. "
    "Focus on delivering a reliable, working solution that meets the client's core needs. "
    "Keep it under 150 words. "
    "CRITICAL RULES: "
    "1. DO NOT overpromise or use overly complex enterprise jargon (e.g., 'sub-second accuracy', 'high volatility'). "
    "2. DO NOT include a 'Subject:' line. "
    "3. DO NOT use placeholders like [Your Name]. "
    "4. Start directly with 'Hi,' or 'Hello,'. "
    "5. Sign the proposal exactly as 'Best regards, VelarixDev'."
)

# FSM States
class JobStates(StatesGroup):
    waiting_for_job = State()

async def get_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error(f"Error: {TOKEN_FILE} not found.")
        sys.exit(1)

def get_regeneration_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🔄 Сгенерировать другой вариант", 
        callback_data="regenerate"
    ))
    return builder.as_markup()

async def main():
    token = await get_token()
    if not token:
        logger.error("Token is empty. Check your token.txt file.")
        return

    # Initialize Bot and Dispatcher
    bot = Bot(token=token)
    dp = Dispatcher()

    # Initialize OpenAI client for local LLM
    client = AsyncOpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY
    )

    @dp.message()
    async def handle_message(message: types.Message, state: FSMContext):
        if not message.text:
            return

        # Save job text and initial temperature to state
        await state.update_data(job_text=message.text, current_temp=0.7)
        await state.set_state(JobStates.waiting_for_job)

        # 1. Send initial status message
        await message.answer("⏳ Анализирую заказ и пишу отклик...")

        try:
            # 2. Request from local LLM
            response = await client.chat.completions.create(
                model="gemma-4-26b-a4b-it",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message.text}
                ],
                temperature=0.7,
            )

            answer = response.choices[0].message.content

            # 3. Send the answer back to user with Inline Keyboard
            await message.answer(answer, reply_markup=get_regeneration_keyboard())

        except Exception as e:
            logger.error(f"Error during LLM request: {e}")
            await message.answer(f"❌ Произошла ошибка при обращении к нейросети: {str(e)}")

    @dp.callback_query(F.data == 'regenerate')
    async def handle_regeneration(callback: CallbackQuery, state: FSMContext):
        # 1. Get data from state
        data = await state.get_data()
        job_text = data.get("job_text")
        current_temp = data.get("current_temp", 0.7)

        if not job_text:
            await callback.answer("Ошибка: текст не найден", show_alert=True)
            return

        # Calculate new temperature logic
        new_temp = round(current_temp + 0.2, 1)
        if new_temp > 1.3:
            new_temp = 0.5
        
        await state.update_data(current_temp=new_temp)
        logger.info(f"Regenerating with temperature: {new_temp}")

        # 2. Update message to loading status (removing buttons)
        try:
            await callback.message.edit_text("⏳ Переписываю отклик...")
        except Exception as e:
            logger.error(f"Error editing message for loading: {e}")
            await callback.answer("Ошибка при обновлении сообщения")
            return

        # 3. Make new request with calculated temperature
        try:
            response = await client.chat.completions.create(
                model="gemma-4-26b-a4b-it",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": job_text}
                ],
                temperature=new_temp,
            )

            new_answer = response.choices[0].message.content

            # 4. Edit message with new answer and button
            await callback.message.edit_text(
                new_answer, 
                reply_markup=get_regeneration_keyboard()
            )
        except Exception as e:
            logger.error(f"Error during regeneration request: {e}")
            await callback.message.edit_text(f"❌ Ошибка при генерации нового варианта: {str(e)}")
        finally:
            # 5. Always answer the callback
            await callback.answer()

    logger.info("Bot is starting...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())