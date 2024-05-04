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


@dp.message(CommandStart())
async def start(message: Message):
    db = DB('user')
    db.new_user(user_id=message.from_user.id, name=message.from_user.first_name, surname=message.from_user.last_name)
    await message.answer('Добро пожаловать',  reply_markup=main_kb)



#Профиль пользователя
@dp.callback_query(F.data == 'profile')
async def profile(call: CallbackQuery):
    db = DB('user')
    db.check_profile(call.from_user.id)
    await call.message.edit_text(f'Профиль пользователя\n\nВас зовут: {db.name} {db.surname}\nРефералов: {db.reffs}')

async def main():
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
