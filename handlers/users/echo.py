from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("👨🏻‍💼💬: Agar yordam kerak bo'lsa /start buyrug'ini jo'nating", reply_markup=ReplyKeyboardRemove())
