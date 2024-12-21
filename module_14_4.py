from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from crud_functions import get_all_products
product_sq = get_all_products()

from config import *
from keyboards import *
import texts

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    '''
    UserState  для определения группы состояний пользователя в Telegram-боте
    Объекты класса State
    age возраст
    groth рост
    weght вес
    '''
    age: int = State()
    growth: int = State()
    weight: int = State()
    gender: str = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(texts.text_start, reply_markup=kb)


@dp.message_handler(text=['Информация'])
async def start_message(message):
    await message.answer(texts.text_info)


@dp.message_handler(text=['Рассчитать'])
@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(texts.text_start, reply_markup=kb_in1)


@dp.message_handler(text=['Купить'])
async def get_buy_list(message):
    for product in product_sq:
        id, title, description, price = product
        await message.answer(f'Название: {title} |\n '
                             f'Описание: {description.replace("        ", " ")} |\n '
                             f'Цена: {price} руб.')
        with open(f'Files/{id}product.png', 'rb') as img:
            await message.answer_photo(img)

    await message.answer(f'{texts.text_select_prod} ',
                         reply_markup=catalog_kb)


@dp.callback_query_handler(text='formulas')
async def send_confirm_message(call_in):
    await call_in.message.answer(texts.text_formulas)
    await call_in.answer()


@dp.callback_query_handler(text=['product_buying'])
async def set_confirm_message(call_in):
    await call_in.message.answer(f'Вы успешно приобрели продукт !')
    await call_in.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call_in):
    try:
        await call_in.message.answer('Введите свой возраст:')
        # @dp.message_handler выводит сообщение Telegram-бот
        await UserState.age.set()
        await call_in.answer()
    except:
        await call_in.message.answer('Ввели неправильный тип данных!')


@dp.message_handler(state=UserState.age)
# Обернунуть set_age(message) в message_handler,
# который реагирует на текстовое сообщение
async def set_growth(message, state):
    try:
        await state.update_data(age=int(message.text))
        await message.answer('Введите свой рост:')
        await UserState.growth.set()
    except:
        await message.answer('Ввели неправильный тип данных!')


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    try:
        await state.update_data(growth=int(message.text))
        await message.answer('Введите свой вес:')
        await UserState.weight.set()
    except:
        await message.answer('Ввели неправильный тип данных!')


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    try:
        await state.update_data(weight=int(message.text))
        await message.answer('Выбрать категорию', reply_markup=start_menu)
        await UserState.gender.set()
    except:
        await message.answer('Ввели неправильный тип данных!')


@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    # расчёт калорий для категорий мужчина.женщина
    try:

        await state.update_data(gender=(message.text))
        data_quest = await state.get_data()

        if data_quest['gender'] == 'Для мужчин':
            result = 10 * int(data_quest['weight']) + \
                     6.25 * int(data_quest['growth']) - \
                     5 * int(data_quest['age']) + 5
            gend = data_quest['gender'].lower()

        elif data_quest['gender'] == 'Для женщин':
            result = 10 * int(data_quest['weight']) + \
                     6.25 * int(data_quest['growth']) - \
                     5 * int(data_quest['age']) - 161

            gend = data_quest['gender'].lower()

        await message.answer(f'Ваша норма калорий: {result} ккал в сутки {gend}',
                             reply_markup=kb)
        await state.finish()
    except:
        await message.answer('Ввели неправильный тип данных!', reply_markup=start_menu)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
