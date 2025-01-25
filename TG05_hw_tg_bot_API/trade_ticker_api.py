# выдавать данные о компании США по тикеру

import asyncio

import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
# Для перевода текста устанавливаем модуль googletrans vers 3.1.0a0 и импортируем библиотеку
from googletrans import Translator

from config import TickerTradeInfo_bot, POLYGON_API_KEY

bot = Bot(token=TickerTradeInfo_bot)
dp = Dispatcher()


# Функция перевода текста на русский
def translate_ru(word):
    translator = Translator()
    result = translator.translate(word, dest='ru')
    return result.text


# функция для получения данных по тикеру
def get_ticker_info(ticker):
    url = f'https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}'
    # отправляем запрос
    response = requests.get(url)
    # Проверка ответа
    if response.status_code == 200:
        # получаем json формат ответа
        return response.json()
    else:
        return None


@dp.message(CommandStart())
async def start(message: Message):  # (атрибут: Тип данных)
    await message.answer(f'Привет, {message.from_user.first_name}, можешь спросить меня про тикеры компаний США')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\n/start \n/help \n/ticker_info ")



# Создаём асинхронную функцию, которая будет брать всю информацию,
# полученную из переменной ticker_info.
@dp.message(Command("ticker_info"))
async def ask_city(message: Message):
    await message.answer("Пожалуйста, введите название тикера:")

    @dp.message()
    async def send_ticker_info(message: Message):
        ticker = message.text.upper()
        ticker_info = get_ticker_info(ticker)
        if ticker_info and 'results' in ticker_info:
            try:
                description_ru = translate_ru(ticker_info['results']['description'])
                info = (
                    f"Название компании - {ticker_info['results']['name']}\n"
                    f"Адрес штаб-квартиры - {ticker_info['results']['address']['address1']}\n"
                    f"Город штаб-квартиры - {ticker_info['results']['address']['city']}\n\n"
                    f"Описание компании - {description_ru}\n\n"
                    f"Зарегистрированное количество выпущенных акций - {ticker_info['results']['share_class_shares_outstanding']}\n"
                )
                await message.answer(info)
            # Обработка ошибки KeyError
            except KeyError:
                await message.answer("Некоторые данные о компании отсутствуют. Попробуйте другой тикер.")
        else:
            await message.answer("Тикер не найден. Попробуйте еще раз.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
