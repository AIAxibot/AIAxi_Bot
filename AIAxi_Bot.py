import os
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_TOKEN'
OPENROUTER_API_KEY = 'YOUR_OPENROUTER_API_KEY'
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Настройка OpenAI
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, подключенный к нейросети через OpenRouter. Задай мне вопрос!")

# Обработчик текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=message.text,
            max_tokens=150
        )
        await message.reply(response.choices[0].text.strip())
    except Exception as e:
        logging.error(f"Ошибка при обращении к OpenAI: {e}")
        await message.reply("Произошла ошибка при обработке вашего запроса.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
