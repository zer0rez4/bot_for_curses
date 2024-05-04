import asyncio
import sys
import logging
import os

from dotenv import load_dotenv

from aiogram import Dispatcher, Bot, types, F

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db_class import DB

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


#расписать все кнопки для main_kb и придумать что поместить под 1-3 (да и просто продумать систему, из нормального тут только профиль)
main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='1', callback_data='1'),  InlineKeyboardButton(text='2', callback_data='2'), InlineKeyboardButton(text='3', callback_data='3')],  [InlineKeyboardButton(text='Курсы', callback_data='courses')], [InlineKeyboardButton(text='Профиль', callback_data='profile')]])
profile_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Изменить имя и фамилию', callback_data='change_name')], [InlineKeyboardButton(text='Назад', callback_data='back')]])

back_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])

@dp.message(CommandStart())
async def start(message: Message):
    db = DB('user')
    db.new_user(user_id=message.from_user.id, name=message.from_user.first_name, surname=message.from_user.last_name)
    await message.answer('Добро пожаловать',  reply_markup=main_kb)

@dp.callback_query(F.data == 'back')
async def main_menu(call: CallbackQuery):
    await call.message.edit_text('Главное меню', reply_markup=main_kb)


#Профиль пользователя
@dp.callback_query(F.data == 'profile')
async def profile(call: CallbackQuery):
    db = DB('user')
    db.check_profile(call.from_user.id)
    await call.message.edit_text(f'Профиль пользователя\n\nВас зовут: {db.name} {db.surname}\nРефералов: {db.reffs}', reply_markup=profile_kb)


@dp.callback_query(F.data == 'change_name')
async def change_name(call: CallbackQuery):
    await call.message.edit_text('Как мне к вам обращаться?')
    dp.message.register(change_data)

async def change_data(message: Message):
    db = DB('user')
    new_name = message.text.split()
    db.name_changer(message.from_user.id, new_name[0], new_name[1])
    await message.answer('Данные успешно изменены', reply_markup=back_kb)


async def main():
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
