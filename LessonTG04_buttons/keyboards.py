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
   [KeyboardButton(text="Тестовая кнопка 1")],
   [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
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
#    [InlineKeyboardButton(text="Видео", url='<https://www.youtube.com/watch?v=HfaIcB4Ogxk>')]
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