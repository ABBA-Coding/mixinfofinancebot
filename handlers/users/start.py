from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_inline import *
from utils.db_api import database as commands
from loader import dp, bot
from utils.db_api.database import *
import datetime


@dp.channel_post_handler(lambda message: message.text in ['SendPostNotification'], state='*')
async def bot_start(message: types.Message, state: FSMContext):
    users = await get_users()
    if datetime.datetime.now().hour == 17:
        asks = await get_client_pay()
        asks_tomorrow = await get_client_pay2()
        for user in users:
            try:
                await bot.send_message(chat_id=user.user_id, text=f'{asks}\n\n{asks_tomorrow}')
            except:
                pass
    # elif datetime.datetime.now().hour == 17:
    #     asks = await get_client_pay2()
    #     for user in users:
    #         await bot.send_message(chat_id=user.user_id, text=asks)
    else:
        pass


@dp.channel_post_handler(lambda message: message.text in ['SendPostNotification5'], state='*')
async def bot_start(message: types.Message, state: FSMContext):
    users = await get_users()
    asks = await get_client_pay2()
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id, text=asks)
        except:
            pass


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}👋. \nMix Info moliyaviy 💶 yordamchisiga xush kelibsiz."
        "\n\nBotdan foydalanish uchun maxsus 🆔 kiriting👇.")
    await state.set_state("auth")


@dp.message_handler(state='auth')
async def get_id(message: types.Message, state: FSMContext):
    if message.text != "mixinfo123":
        await message.answer("Ushbu maxsus id royxatda mavjud emas⚠️. \nQaytadan urinib ko'ring 🔄")
    else:
        await add_user(message.from_user.id)
        if await chek_user(message.from_user.id):
            markup = await admin_menu()
            await message.answer("✅ Maxsus 🆔 to'g'ri kitildi.\n\n 👨🏻‍💼 Yordamchi sizga yordamga tayyor.",
                                 reply_markup=markup)
            await state.set_state("get_command")
        else:
            markup = await ask_keyboard()
            await message.answer("✅ Maxsus 🆔 to'g'ri kitildi.\n\n 👨🏻‍💼 Yordamchi sizga yordamga tayyor.",
                                 reply_markup=markup)
            # await state.set_state("ask_money")
            await state.set_state("get_command")


@dp.message_handler(state='get_command')
async def get_id(message: types.Message, state: FSMContext):
    command = message.text
    if command not in ["Eslatma qo'shish", "To'lov eslatmasi qo'shish"]:
        await message.answer("☹️ Buyruqni tushunarsiz.\nIltimos buyruqlar to'plamidan foydalaning 👇.")
    else:
        if command == "Eslatma qo'shish":
            await message.answer("To'lov qabul qilinishi kerak bo'lgan Mijoz nomini kiriting👇.")
            await state.set_state("get_client")
        else:
            await message.answer("To'lov qilinishi kerak bo'lgan xizmat nomini kiritig")
            await state.set_state("payment_name")


@dp.message_handler(state='payment_name')
async def get_id(message: types.Message, state: FSMContext):
    markup = await back_keyboard()
    await message.answer("Oyning qaysi kunida eslatma eslatilsin", reply_markup=markup)
    await state.update_data(payment_name=message.text)
    await state.set_state("payment_date")


@dp.message_handler(state='get_client')
async def get_id(message: types.Message, state: FSMContext):
    markup = await back_keyboard()
    await message.answer("👨🏻‍💼💬: Kerakli summani sonlarda kiriting👇", reply_markup=markup)
    await state.update_data(client_name=message.text)
    await state.set_state("client_amount")


@dp.message_handler(state='payment_date')
async def get_id(message: types.Message, state: FSMContext):
    d = message.text
    if d.isnumeric():
        markup = await back_keyboard()
        await message.answer("To'lov summasini kiriting", reply_markup=markup)
        await state.update_data(date=message.text)
        await state.set_state("payment_amount")
    elif d == "⬅️ Bekor qilish":
        markup = await admin_menu()
        await message.answer("👨🏻‍💼💬: Bekor qilindi.", reply_markup=markup)
        await state.set_state("get_command")
    else:
        await message.answer("😳 Sanani raqamlarda kiriting.")


@dp.message_handler(state='payment_amount')
async def get_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text != "⬅️ Bekor qilish":
        if message.text.isnumeric():
            name = data['payment_name']
            date = data['date']
            resutl = await add_payment(client=name, date=date, amount=message.text)
            if resutl is not None:
                markup = await admin_menu()
                await message.answer("Eslatma qabul qilindi✅.", reply_markup=markup)
                await state.set_state("get_command")
            else:
                await message.answer("Xatolik ⚠️.\n\nQaytadan kiriting👇")
        else:
            await message.answer("😳 Summani raqamlarda kiriting.")

    else:
        markup = await admin_menu()
        await message.answer("👨🏻‍💼💬: Bekor qilindi.", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state='client_amount')
async def get_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text != "⬅️ Bekor qilish":
        if message.text.isnumeric():
            markup = await back_keyboard()
            await state.update_data(amount=message.text)
            await message.answer("Belgilangan 📅 sanani 2022-08-11 tarzida kiriting", reply_markup=markup)
            await state.set_state("client_date")
        else:
            await message.answer("😳 Summani raqamlarda kiriting.")
    else:
        markup = await admin_menu()
        await message.answer("👨🏻‍💼💬: Bekor qilindi.", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state='client_date')
async def get_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text != "⬅️ Bekor qilish":
        name = data['client_name']
        amount = int(data['amount'])
        resutl = await add_client_pay(client=name, date=message.text, amount=amount)
        if resutl is not None:
            markup = await admin_menu()
            await message.answer("Eslatma qabul qilindi✅.", reply_markup=markup)
            await state.set_state("get_command")
        else:
            await message.answer("Xatolik ⚠️.\n\nQaytadan kiriting👇")
    else:
        markup = await admin_menu()
        await message.answer("👨🏻‍💼💬: Bekor qilindi.", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state='ask_money')
async def get_id(message: types.Message, state: FSMContext):
    if message.text != "💵 Avans so'rash":
        await message.answer("☹️ Buyruqni tushunarsiz.\nIltimos buyruqlar to'plamidan foydalaning 👇.")
    else:
        markup = await back_keyboard()
        await message.answer("Avans kim uchun zarur?\nIltimos Ism Familiyangizni kiriting 👇.", reply_markup=markup)
        await state.set_state("get_name")


@dp.message_handler(state='get_name')
async def get_id(message: types.Message, state: FSMContext):
    if message.text != "⬅️ Bekor qilish":
        await message.answer("Sizga zarur bo'lgan 💲 summani kiriting 👇.")
        await state.update_data(name=message.text)
        await state.set_state("amount_money")
    else:
        markup = await ask_keyboard()
        await message.answer("👨🏻‍💼: Ok, ortga qaytamiz.", reply_markup=markup)
        await state.set_state("ask_money")


@dp.message_handler(state='amount_money')
async def get_id(message: types.Message, state: FSMContext):
    summa = message.text
    data = await state.get_data()
    if summa.isnumeric():
        name = data['name']
        users = await get_users()
        markup = await ask_keyboard()
        await add_avans(user_id=message.from_id, name=name, summa=summa)
        text = f"👨🏻‍💼💬: Yangi avans so'rovi yetib keldi.\n\n<b>Kimga </b>: {name}.\n<b>Summa</b> : {message.text}\n\n<b>Kim tomonidan jo'natildi </b>: {message.from_user.first_name}|https://t.me/{message.from_user.username}\n"
        for user in users:
            await bot.send_message(chat_id=user.user_id, text=text, parse_mode="HTML")
        await message.answer("👨🏻‍💼💬: Avans so'rovi jo'natildi", reply_markup=markup)
    else:
        await message.answer("😳 Summani raqamlarda kiriting.")
