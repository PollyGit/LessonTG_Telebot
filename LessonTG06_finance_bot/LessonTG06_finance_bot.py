# разработаем кейс "Финансовый бот-помощник"
# 1) Посмотреть курс валют через API
# 2)возможность вести учет финансов расход по 3 категориям
# 3) регистрация
# 4) Советы по экономии

import asyncio
import logging
import random
import sqlite3

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import Finance_bot

bot = Bot(token=Finance_bot)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Создание кнопок в ТГ боте
button_registr = KeyboardButton(text="Регистрация в телеграм боте")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы по экономии")
button_finances = KeyboardButton(text="Личные финансы")

# Создание клавиатуры с этими кнопками, в 2 ряда
keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_tips, button_finances]
], resize_keyboard=True)

# Работа с БД user.db
conn = sqlite3.connect('user.db')
cursor = conn.cursor()
# Создание таблицы
# Где UNIQUE - уникальные значения, 3 категории и 3 категории расходов
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL
    )
''')

# сохранение после выполнения этого действия
conn.commit()


# Чтобы запрашивать информацию и ждать ответа, нужно использовать состояния.
# Создаём класс, в котором будут прописаны эти состояния для каждой категории
# и каждого значения категории.
class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()


# Базовая ф-ция Старт
@dp.message(Command('start'))
async def send_start(message: Message):
    await message.answer("Привет! Я ваш личный финансовый помощник. Выберите одну из опций в меню:",
                         reply_markup=keyboards)


# Прописываем декоратор для регистрации в боте.
# В кавычках указываем текст, который будет вызывать работу этой функции.
@dp.message(F.text == "Регистрация в телеграм боте")
async def registration(message: Message):
    # Сохраняем  ID пользователя, который отправил боту сообщение. И Имя.
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    # Проверяем существование пользователя в таблице
    # В ? подставляется значение из переменной  telegram_id
    # с помощью действия с курсором
    cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    # будет брать первый попавшийся результат
    user = cursor.fetchone()
    if user:
        await message.answer("Вы уже зарегистрированы!")
    else:
        # если юзер не существует, то вставляем информацию (telegram_id, name)
        cursor.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        # Сохранить изменения
        conn.commit()
        await message.answer("Вы успешно зарегистрированы!")


# Создаём функцию, которая будет выдавать курс валют.
# Создаём декоратор и асинхронную функцию.
@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/e4737de1a5a55d8038eb39bd/latest/USD"
    try:
        # запрос по адресу url
        response = requests.get(url)
        data = response.json()
        # Прописываем проверку (если статус-код не равен 200, то есть не успешен).
        if response.status_code != 200:
            await message.answer("Не удалось получить данные о курсе валют!")
            return
        # смотрим коэф конвертации в JSON
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']
        # Перевод Евро в Рубли
        euro_to_rub = eur_to_usd * usd_to_rub
        # отправка ответа так, чтобы число было с 2 знаками после запятой (2f)
        await message.answer(f"1 USD - {usd_to_rub:.2f}  RUB\n"
                             f"1 EUR - {euro_to_rub:.2f}  RUB")

    except:
        await message.answer("Произошла ошибка")


# Создаём асинхронную функцию для отправки текста с советами по экономии
@dp.message(F.text == "Советы по экономии")
async def send_tips(message: Message):  # отправляет просто текст
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
    ]
    tip = random.choice(tips)
    await message.answer(tip)


# Работаем с личными финансами
@dp.message(F.text == "Личные финансы")
# Создаём асинхронную функцию, работа с состояниями: Вводим второй атрибут функции
async def finances(message: Message, state: FSMContext):
    # Устанавливаем новое состояние.
    # В круглых скобках указываем класс и категорию этого состояния.
    await state.set_state(FinancesForm.category1)
    # Отправляем сообщение пользователю, что ждем ответа
    await message.reply("Введите первую категорию расходов:")


# Создаём декоратор, который сработает не по фразе, а по категории
@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
    # Настраиваем обновление данных.
    # Теперь в category1 будет сохраняться текст сообщения.
    await state.update_data(category1=message.text)
    # Начинаем использовать новое состояние.
    # Значение денег, которые уходят на эту категорию товаров.
    await state.set_state(FinancesForm.expenses1)
    await message.reply("Введите расходы для категории 1:")


#Прописываем функцию, которая сработает после получения предыдущего значения.
@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.reply("Введите вторую категорию расходов:")


#Создаём функцию для расходов по второй категории.
@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply("Введите расходы для категории 2:")


@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.reply("Введите третью категорию расходов:")


#Создаём функцию для расходов по 3 категории.
@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply("Введите расходы для категории 3:")


@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    #Создаём переменную data, в которую сохраним всю информацию по состояниям.
    data = await state.get_data()
    #Сохраняем telegram ID пользователя,
    # чтобы сохранить информацию в нужную строчку базы данных.
    telegarm_id = message.from_user.id
    #Отравляем запрос
    #Обновляем информацию и устанавливаем значения для категорий в базе данных
    cursor.execute(
        '''UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ? WHERE telegram_id = ?''',
        (data['category1'], data['expenses1'], data['category2'], data['expenses2'], data['category3'],
         float(message.text), telegarm_id))
    conn.commit()
    #Очищаем состояния.
    await state.clear()

    await message.answer("Категории и расходы сохранены!")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
