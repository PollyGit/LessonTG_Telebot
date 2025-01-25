# мы пишем название породы и бот выдаёт информацию
# и фотографию котика этой породы.

import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, THE_CAT_API_KEY

# Для перевода текста устанавливаем модуль googletrans vers 3.1.0a0 и импортируем библиотеку
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Вот в этом промежутке мы будем работать и писать новый код

# Функция перевода текста на русский
def translate_pt(word):
    translator = Translator()
    result = translator.translate(word, dest='ru')
    return result.text


# Пишем функцию для получения списка пород кошек
# Добавляем URL из документации (апи ключ как заголовок)
def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    # Прописываем заголовок, запрос и возвращение
    # первого элемента ответа. Ответ сохраняем в переменную.
    headers = {"x-api-key": THE_CAT_API_KEY}  # так просят исп-ть в док-ции
    response = requests.get(url, headers=headers)
    return response.json()


# Теперь нам нужно получить информацию о породе кошки.
# Пишем функцию для получения информации (картинки кошки) по породе:
def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    # вернуть первый элемент(ссылку)
    return data[0]['url']


# получить информацию о породе кошки
# Функция для получения информации о породе кошек
def get_breed_info(breed_name):
    # здесь будут сохраняться все породы
    breeds = get_cat_breeds()
    # Перебираем породы внутри их списка
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():  # сравниваем имя
            return breed
    return None


# оформляем полученную информацию.
# Пишем стартовую функцию
# @dp.message(Command('cats'))
# @dp.message(CommandStart())
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши мне название породы кошки, и я пришлю тебе её фото и описание.")


# и  основную функцию вконце
@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    # берем инфо из ф-ции выше
    # breed_info принимает информацию, включая id  породы
    breed_info = get_breed_info(breed_name)
    # Проверка наличия инфо об этой породе
    if breed_info:
        # используем функцию выше для получения информации о породе
        #
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        info = (
            f"Порода - {breed_info['name']}\n"
            f"Описание - {breed_info['description']}\n"
            f"Темперамент -  {breed_info['temperament']}\n"
            f"Продолжительность жизни - {breed_info['life_span']} лет"
        )
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer("Порода не найдена. Попробуйте еще раз.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
