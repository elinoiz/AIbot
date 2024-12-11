
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import requests


API_TOKEN = '7646001687:AAEQCEwB3eDHnZSxoeOJ7F40D2_4Rd-Kppg'
MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions'
MISTRAL_API_KEY = 'Rej7dFCCWSbzQtYs4CsSZsjByBn3uYwt'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который использует Mistral API. Задайте мне вопрос!")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    user_message = message.text
    response = make_mistral_request(user_message)
    await message.reply(response)

# Функция для выполнения запроса к Mistral API
def make_mistral_request(query: str) -> str:
    headers = {
        'Authorization': f'Bearer {MISTRAL_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Вызовет исключение для HTTP ошибок
        logging.info(f"Response from Mistral API: {response.json()}")
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', 'Не удалось получить ответ.')
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return f"HTTP ошибка: {http_err}"
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return f"Ошибка: {err}"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




