import os
import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio

# Загружаем переменные API
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Устанавливаем API-ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Настройка бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработчик сообщений
@dp.message()
async def chatgpt_reply(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "Ошибка при обработке запроса."
        logging.error(f"Ошибка OpenAI: {e}")

    await message.answer(reply)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
