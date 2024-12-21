# Бот прогноза погоды для конкретного пользователя и города пользователя


import asyncio
# логгирование
import logging
import sqlite3

# для сохранения состояния в оперативной памяти
# для выполнения асинхронных HTTP-запросов
import aiohttp
# импортируем не всю библиотеку, а только Бот и Диспетчер
# специальный класс F, который позволяет прописывать условия на получение сообщения
from aiogram import Bot, Dispatcher
# .filters - отлавливание определенных команд
# Чтобы отслеживать команды, нужно импортировать фильтры и типы сообщений
# FSInputFileОн необходим для обработки файлов и их отправки в aiogram.
from aiogram.filters import CommandStart
# для сохранения контекста между сообщениями
from aiogram.fsm.context import FSMContext
# Библиотека для работы с состояниями
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from configTG03 import TOKEN, TOKEN2

WEATHER_API_KEY = TOKEN2

# Создадим объекты 2х этих классов:
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создание базы данных
# INFO - уровень логгирования
logging.basicConfig(level=logging.INFO)


# работа с состояниями
class Form(StatesGroup):
    name = State()
    age = State()
    city = State()


# создаем базу данных users, в которую будет
# сохраняться информация от пользователя:
def init_db():
    conn = sqlite3.connect('user_data.db')  # Cоздать подключение к бд
    cur = conn.cursor()  # создаем курсор
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL)''')
    # сохраняем изменения
    conn.commit()
    # закрываем подключение
    conn.close()


# Чтобы запустить программу
init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    # Сохранить состояние и ожидание ответа от пользователя
    await state.set_state(Form.name)


# После получения имени от пользователя, запускается эта ф-ция
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    # сохранять введенное имя пользователя в текст сообщения в контексте состояния
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)


@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    # сохраняет все данные, которые были сохранены в контексте состояния,
    # и из этого создает словарь
    user_data = await state.get_data()

    # добавить информацию (в переменной user_data) в базу данных:
    conn = sqlite3.connect('user_data.db')  # Подключение к БД
    cur = conn.cursor()  # Создаем курсор
    # INSERT INTO - вставляем данные в БД
    # Прописываем, что будет подставляться вместо
    # этих вопросительных знаков
    cur.execute('''
       INSERT INTO users (name, age, city) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()  # Сохраняем
    conn.close()  # закрываем подключение

    # создаем асинхронную сессию клиента
    async with aiohttp.ClientSession() as session:
        # выполняем HTTP-запрос с помощью метода get
        async with session.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={WEATHER_API_KEY}&units=metric") as response:
            if response.status == 200:
                weather_data = await response.json()
                main = weather_data['main']
                # азбираем данные из формата json
                weather = weather_data['weather'][0]
                temperature = main['temp']
                humidity = main['humidity']
                description = weather['description']

                # Сохраняем все в одно сообщение
                weather_report = (f"Город - {user_data['city']}\n"
                                  f"Температура - {temperature}\n"
                                  f"Влажность воздуха - {humidity}\n"
                                  f"Описание погоды - {description}")
                # Отправляем сообщение
                await message.answer(weather_report)
            else:
                await message.answer("Не удалось получить данные о погоде")
        # очистить состояния
        await state.clear()


# Создадим асинхронную функцию main, которая будет запускать наш бот
async def main():
    # действие, которое происходит с Telegram-ботом
    await dp.start_polling(bot)
    # dp.start_polling - программа будет отправлять запрос в Telegram, проверяя,
    # есть ли входящие сообщения и произошедшие события.


if __name__ == "__main__":
    # функция здесь асинхронная, ее нужно запускать определенным образом,
    # указывая при этом, какую именно функцию мы хотим запустить
    asyncio.run(main())
