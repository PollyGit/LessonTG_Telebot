import asyncio

# импортируем не всю библиотеку, а только Бот и Диспетчер
# специальный класс F, который позволяет прописывать условия на получение сообщения
from aiogram import Bot, Dispatcher, F
# .filters - отлавливание определенных команд
# Чтобы отслеживать команды, нужно импортировать фильтры и типы сообщений
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# из файла config импортируем токен телеграмбота
from config import TOKEN, TOKEN2

import random
import requests


# в функции прописываем город, который мы будем вводить в форме
def get_weather(city):
    # личный апи ключ с сайта
    api_key = TOKEN2
    # city = 'Moscow'
    #city = 'Sankt Petersburg'
    # адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    # для получения результата нам понадобится модуль requests
    response = requests.get(url)
    # прописываем формат json возврата результата
    return response.json()


# Bot и Dispatcher — это два компонента, которые есть в aiogram.
# Bot отвечает за взаимодействие с Telegram bot API,
# а Dispatcher управляет обработкой входящих сообщений и команд.

# Создадим объекты 2х этих классов:
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Создадим декоратор для обработки команды /start
# Хендлер (Handler) — это функция, выполняющая
# определенное действие в ответ на событие.
@dp.message(CommandStart())
async def start(message: Message):  # (атрибут: Тип данных)
    # Действие - ответ на команду /start
    await message.answer("Приветики, я бот, расскажу тебе про погоду!")


# хендлер для “отлавливания” команды help
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start \n/help \n/photo \n/weather \n/town")


# хендлер для “отлавливания” команды погода
@dp.message(Command('weather'))
async def weather(message: Message):
    city = 'Sankt Petersburg'
    weather_data = get_weather(city)
    if weather_data.get("main") and weather_data.get("weather"):
        temperature = weather_data["main"]["temp"]
        weather_description = weather_data["weather"][0]["description"]
        await message.answer(f"Погода такая в {city}: {temperature}°C, {weather_description}")
    else:
        await message.answer("Не удалось получить данные о погоде.")


@dp.message(Command('town'))
async def ask_city(message: Message):
    await message.answer("Пожалуйста, введите название города:")

    @dp.message()
    async def get_city_and_weather(message: Message):
        city = message.text
        weather_data = get_weather(city)
        if weather_data.get("main") and weather_data.get("weather"):
            temperature = weather_data["main"]["temp"]
            weather_description = weather_data["weather"][0]["description"]
            await message.answer(f"Погода такая в {city}: {temperature}°C, {weather_description}")
        else:
            await message.answer("Не удалось получить данные о погоде.")


# Создадим асинхронную функцию main, которая будет запускать наш бот
async def main():
    # действие, которое происходит с Telegram-ботом
    await dp.start_polling(bot)
    # dp.start_polling - рограмма будет отправлять запрос в Telegram, проверяя,
    # есть ли входящие сообщения и произошедшие события.


#Прописываем хендлер и варианты ответов на сообщение и на фото
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(Command('photo'))
async def photo(message: Message):
    list2 = ['https://lenis-animal.ru/wp-content/uploads/2016/07/pogoda.jpg', 'https://mimer.ru/content/ckfinder/userfiles/images/метео3.jpg', 'https://mimer.ru/content/ckfinder/userfiles/images/метео2.jpg']
    rand_photo = random.choice(list2)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')



if __name__ == "__main__":
    # функция здесь асинхронная, ее нужно запускать определенным образом,
    # указывая при этом, какую именно функцию мы хотим запустить
    asyncio.run(main())
