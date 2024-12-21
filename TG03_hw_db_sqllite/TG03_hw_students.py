# Телеграм-бота, который запрашивает у пользователя имя, возраст и класс.
# Сохраняет введенные данные в таблицу students базы данных school_data.db.


import asyncio
# логгирование
import logging
import sqlite3
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
from configTG03hw import TOKEN


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
    grade = State()


# создаем базу данных users, в которую будет
# сохраняться информация от пользователя:
def init_db():
    conn = sqlite3.connect('school_data.db')  # Cоздать подключение к бд
    cur = conn.cursor()  # создаем курсор
    cur.execute('''
        CREATE TABLE IF NOT EXISTS school_data (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)''')
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
    await message.answer("Из какого ты класса?")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def city(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    # сохраняет все данные, которые были сохранены в контексте состояния,
    # и из этого создает словарь
    school_data = await state.get_data()

    # добавить информацию (в переменной user_data) в базу данных:
    conn = sqlite3.connect('school_data.db')  # Подключение к БД
    cur = conn.cursor()  # Создаем курсор
    # INSERT INTO - вставляем данные в БД
    # Прописываем, что будет подставляться вместо
    # этих вопросительных знаков
    cur.execute('''
       INSERT INTO school_data (name, age, grade) VALUES (?, ?, ?)''',
                (school_data['name'], school_data['age'], school_data['grade']))
    conn.commit()  # Сохраняем
    conn.close()  # закрываем подключение

    student_report = (f"Класс - {school_data['grade']}\n"
                      f"Имя - {school_data['name']}\n"
                      f"Возраст - {school_data['age']}\n")
    # Отправляем сообщение
    await message.answer(student_report)
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
