# Кнопки и клавиатуры

# импортируем возможность создавать клавиатуры и возможность создавать кнопки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# Для подключения билдера
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# 1
# Создаём клавиатуру для Reply-кнопок
# создаём переменную, в которой будет храниться
# клавиатура и которую мы подключим к боту.
main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)
# Каждый отдельный список — это ряд клавиатуры.

# 2
# Создаём клавиатуру для Inline-кнопок
# И обязательно добавить ссылку или колбеки в атрибуты
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
   [InlineKeyboardButton(text="Новости", callback_data='news')],
   [InlineKeyboardButton(text="Профиль", callback_data='person')]
])

# inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')]
# ])



# 3
# Конструируем билдер Reply

# создаём список с четырьмя кнопками
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

# Создаём асинхронную функцию и клавиатуру внутри этой функции
# Добавляем кнопки в клавиатуру keyboard
async def test_keyboard():
   keyboard = ReplyKeyboardBuilder()
   for key in test:
      keyboard.add(KeyboardButton(text=key))
   #2 - 2 кнопки вверху и остальные внизу
   return keyboard.adjust(2).as_markup()


#4
# Конструируем билдер Inline
async def test_keyboard_inline():
   keyboard_in = InlineKeyboardBuilder()
   for key in test:
       keyboard_in.add(InlineKeyboardButton(text=key, url='<https://www.youtube.com/watch?v=HfaIcB4Ogxk>'))
   return keyboard_in.adjust(2).as_markup()




#клавиатуры для дз

inline_keyboard_links = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url='https://dzen.ru/news')],
   [InlineKeyboardButton(text="Музыка", url='https://yandex.ru/video/preview/17697647739932639266')],
   [InlineKeyboardButton(text="Видео", url='https://dzen.ru/shorts/641b155d7013ca298c879dab?sid=138434450155779257')]
])


more = ["Опция 1", "Опция 2"]

inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data='catalog')]
])

async def inline_dynamic():
   inline_dynamic = InlineKeyboardBuilder()
   for key in more:
       inline_dynamic.add(InlineKeyboardButton(text=key, callback_data=key))
   return inline_dynamic.adjust(2).as_markup()