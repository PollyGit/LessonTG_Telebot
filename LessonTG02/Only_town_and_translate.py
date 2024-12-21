import asyncio
import os
import random

import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from config import TOKEN, TOKEN2
from googletrans import Translator
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup


bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    city = State()  # Состояние для ввода города
    translate = State()  # Состояние для ввода текста для перевода


def get_weather(city):
    api_key = TOKEN2
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()


def translate_this(word):
    translator = Translator()
    result = translator.translate(word, dest='en')
    return result.text


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}')


@dp.message(Command('town'))
async def ask_city(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите название города:")
    await state.set_state(Form.city)

@dp.message(StateFilter(Form.city))
async def get_city_and_weather(message: Message, state: FSMContext):
    city = message.text
    weather_data = get_weather(city)
    if weather_data.get("main") and weather_data.get("weather"):
        temperature = weather_data["main"]["temp"]
        weather_description = weather_data["weather"][0]["description"]
        await message.answer(f"Погода в городе {city} такая: {temperature}°C, {weather_description}")
    else:
        await message.answer("Не удалось получить данные о погоде.")
    await state.clear()


@dp.message(Command('translate'))
async def ask_translate(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите текст для перевода:")
    await state.set_state(Form.translate)


@dp.message(StateFilter(Form.translate))
async def translate(message: Message, state: FSMContext):
    sms_ru = message.text
    sms_eng = translate_this(sms_ru)
    await message.answer(sms_eng)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
