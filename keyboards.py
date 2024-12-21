''''''
'''
Верстка клавиатур Bot
'''
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions
from crud_functions import get_all_products

product_sq = get_all_products()

kb = ReplyKeyboardMarkup(input_field_placeholder='Выберите пункт меню. ',
                         resize_keyboard=True)
button1 = KeyboardButton('Рассчитать')
button2= KeyboardButton('Информация')
button3= KeyboardButton('Купить')
kb.row(button1,button2)
kb.add(button3)


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f'{product_sq[0][1]}', callback_data='product_buying'),
        InlineKeyboardButton(text=f'{product_sq[1][1]}', callback_data='product_buying'),
        InlineKeyboardButton(text=f'{product_sq[2][1]}', callback_data='product_buying'),
        InlineKeyboardButton(text=f'{product_sq[3][1]}', callback_data='product_buying')
         ]
    ],resize_keyboard=True
)


kb_in1 = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Расчитать норму калорий',callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas')
kb_in1.add(button1,button2)

start_menu=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Для мужчин'),KeyboardButton(text='Для женщин')
         ]
    ],resize_keyboard=True
)