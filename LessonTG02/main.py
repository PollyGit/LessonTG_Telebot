import asyncio
import os
import random

import requests
# импортируем не всю библиотеку, а только Бот и Диспетчер
# специальный класс F, который позволяет прописывать условия на получение сообщения
from aiogram import Bot, Dispatcher, F
# .filters - отлавливание определенных команд
# Чтобы отслеживать команды, нужно импортировать фильтры и типы сообщений
# FSInputFileОн необходим для обработки файлов и их отправки в aiogram.
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
# gtts - спец библиотека для озвучки текста Google TTS
from gtts import gTTS

# из файла config импортируем токен телеграмбота
from config import TOKEN, TOKEN2


# в функции прописываем город, который мы будем вводить в форме
def get_weather(city):
    # личный апи ключ с сайта
    api_key = TOKEN2
    # city = 'Moscow'
    city = 'Sankt Petersburg'
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


# 1
# Создадим декоратор для обработки команды /start
# Хендлер (Handler) — это функция, выполняющая
# определенное действие в ответ на событие.
@dp.message(CommandStart())
async def start(message: Message):  # (атрибут: Тип данных)
    # Действие - ответ на команду /start
    # await message.answer("Приветики, я бот, расскажу тебе про погоду!")
    # Отвечать персонализированно по Имени
    await message.answer(f'Приветики, {message.from_user.first_name}')


# 2
# хендлер для “отлавливания” команды help
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start \n/help \n/photo \n/weather \n/town \nvideo \naudio \ntraining \ndoc")


# 3
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


# 4
# Создадим асинхронную функцию main, которая будет запускать наш бот
async def main():
    # действие, которое происходит с Telegram-ботом
    await dp.start_polling(bot)
    # dp.start_polling - рограмма будет отправлять запрос в Telegram, проверяя,
    # есть ли входящие сообщения и произошедшие события.


# 5
# Прописываем хендлер и варианты ответов на сообщение и на фото
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


# 6
# @dp.message(F.photo)
# async def react_photo(message: Message):
#     list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
#     rand_answ = random.choice(list)
#     await message.answer(rand_answ)


# 6_1
# Скачивание файлов пользователя. Создать папку tmp/  в проекте.
# ТГ отправляет одно фото сразу в нескольких размерах.
# -1 - самый максимальный доступный размер, те последний в списке.
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


# 7
@dp.message(Command('photo'))
async def photo(message: Message):
    list2 = [
        'https://lenis-animal.ru/wp-content/uploads/2016/07/pogoda.jpg',
        'https://mimer.ru/content/ckfinder/userfiles/images/метео3.jpg',
        'https://mimer.ru/content/ckfinder/userfiles/images/метео2.jpg'
    ]
    rand_photo = random.choice(list2)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


# 7_1
# Работа с префиксами
@dp.message(Command('photo', prefix='&'))
async def photo(message: Message):
    list2 = [
        'https://lenis-animal.ru/wp-content/uploads/2016/07/pogoda.jpg',
        'https://mimer.ru/content/ckfinder/userfiles/images/метео3.jpg',
        'https://mimer.ru/content/ckfinder/userfiles/images/метео2.jpg'
    ]
    rand_photo = random.choice(list2)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


# 9
# создадим команду и функцию для отправки видео:
@dp.message(Command('video'))
async def video(message: Message):
    # уведомление о загрузке видео
    await bot.send_chat_action(message.chat.id, 'upload_video')
    # создадим переменную, в которой будет храниться объект класса,
    # который мы только что импортировали. ('video.mp4') - путь к файлу
    video = FSInputFile('video.mp4')
    # две команды для отправки видео: message.answerVideo или bot.sendVideo
    # указываем ID чата, откуда пришла команда, и переменную video.
    await bot.send_video(message.chat.id, video)


# 10
# создадим команду и функцию для отправки аудио:
@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('sound.mp3')
    await bot.send_audio(message.chat.id, audio)


# 11
# Озвучивание текста
@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n 1. Скручивания: 3 подхода по 15 повторений\n 2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n 3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n 1. Подъемы ног: 3 подхода по 15 повторений\n 2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n 3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n 2. Горизонтальные ножницы: 3 подхода по 20 повторений\n 3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"{message.from_user.first_name}, если погода сегодня не очень, то ты можешь заняться спортом дома. Это твоя мини-тренировка на сегодня {rand_tr}")
    # Создадим объект класса GoogleTTS.
    # Текст для озвучки хранится в переменной rand_tr
    # lang='ru' язык озвучки
    tts = gTTS(text=rand_tr, lang='ru')

    # #Эта часть для отправка аудио файлом закомментирую
    # # сохранить в файл training.mp3 то, что мы создадим
    # tts.save("training.mp3")
    # # эти данные нужно отправить
    # audio = FSInputFile('training.mp3')
    # await bot.send_audio(message.chat.id, audio)
    # # удалить файл после отправки
    # os.remove("training.mp3")

    # Эта часть для отправка аудио сообщением
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove("training.ogg")


# 12
#Отправка голосовых сообщений
# Взять предыдущий код с тренировкой и поменять формат файла на ogg
@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)


# 13
#Отправка документов
@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)


# 8
# Универсальный обработчик сообщений, универсальный декоратор
@dp.message()
async def sms(message: Message):
    await message.answer("Я тебе ответил")


# 8_2
# Отслеживание сообщений с помощью условного оператора
@dp.message()
async def sms(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')


# 8_1
# ЭХО бот
# Указан id чата, откуда получили сообщение и отвечаем
# Его добавлять в код в самом низу
@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


if __name__ == "__main__":
    # функция здесь асинхронная, ее нужно запускать определенным образом,
    # указывая при этом, какую именно функцию мы хотим запустить
    asyncio.run(main())
