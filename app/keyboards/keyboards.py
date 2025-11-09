from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)

#Стартовая клавиатура 
def Inline_keyboard():
    main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список заметок", callback_data='list')],
        [InlineKeyboardButton(text="Добавить", callback_data='add')],
        [InlineKeyboardButton(text="Удалить", callback_data='delete')],
        [InlineKeyboardButton(text="Перечеркнуть", callback_data='cross')]
    ])
    return main