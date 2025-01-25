# выдавать космическое изображение

import asyncio
import random
from datetime import datetime, timedelta

import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


# функция для получения случайного космического изображения дня
def get_random_apod():
    # конечная дата - сегодня
    end_date = datetime.now()
    # дата начала - год назад от сегодня
    start_date = end_date - timedelta(days=365)
    # рандомная дата за последний год
    random_date = start_date + (end_date - start_date) * random.random()
    # формат даты в таком виде, который просит описание АПИ с сайта:
    date_str = random_date.strftime("%Y-%m-%d")

    # переменная-ссылка на гет-запрос
    # изначально ссылка была короче, добавляем в гет-запрос дату
    # т.о.: &date={date_str}
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    # отправляем запрос
    response = requests.get(url)
    # получаем json формат ответа
    return response.json()


# команда "random_apod", которая будет считывать,
# что мы хотим увидеть изображение.
# И Создаём асинхронную функцию, которая будет брать всю информацию,
# полученную из переменной random_apod.
@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    # отдельно сохраняем ссылку на фото и заголовок
    photo_url = apod['url']
    title = apod['title']

    await message.answer_photo(photo=photo_url, caption=f"{title}")

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
