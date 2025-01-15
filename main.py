import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from config import BOT_TOKEN as token, admin, kanal_id
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from states import UserList
from aiogram.fsm.context import FSMContext
from buttons import Tasdiqlash



logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

bot = Bot(token=token)


@dp.message(CommandStart())
async def StartBot(message: Message, state:FSMContext):
    await message.answer("Salom Ismingizni yozing....")
    await state.set_state(UserList.name)


@dp.message(F.text, UserList.name)
async def IsmBot(message: Message, state:FSMContext):
    xabar = message.text
    await state.update_data({'ism':xabar})
    await message.answer(f"Tanishganimdan Xursandman {xabar}\nBot yasashga qiziqasizmi?")
    await state.set_state(UserList.interesting)

@dp.message(F.text, UserList.interesting)
async def User1Bot(message: Message, state: FSMContext):
    xabar = message.text
    print(xabar)
    if xabar.lower() == "ha":
        await message.answer(f"Qaysi dasturlash tilidan foydalanasiz")
        await state.update_data({'xabar':xabar})
        await state.set_state(UserList.code)
    elif xabar.lower() == 'yoq':
        await message.answer("Bu ham yomon emas keyinroq ko'rishamiz")
        await state.clear()
    else:
        await message.answer("Qiziqish uchun ha yoki yoq kiriting ?")
        await state.set_state(UserList.interesting)


@dp.message(F.text, UserList.code)
async def CodeBot(message: Message, state: FSMContext):
    dastulash = message.text
    await state.update_data({"coder":dastulash})
    await message.answer("Qaysi companiyada ishlaysiz")
    await state.set_state(UserList.finish)


@dp.message(F.text, UserList.finish)
async def FinishBot(message: Message, state: FSMContext):
    companiya = message.text
    await state.update_data(companiya=companiya)
    data = await state.get_data()
    ism = data.get("ism")
    xabar = data['xabar']
    dasturlash = data.get('coder')
    companiya = data.get('companiya')
    await message.answer(f"Ism: {ism}\nxabar: {xabar}\ndasturlash tili: {dasturlash}\nIsh joyi: {companiya}\nSizning malumotlaringiz saqlanish uchun jonatilsinmi ?", reply_markup=Tasdiqlash)
    await state.set_state(UserList.admin)


@dp.callback_query(F.data, UserList.admin)
async def  AdminBot(call: CallbackQuery, state: FSMContext):
    xabar = call.data
    if xabar == 'ha':
        data = await state.get_data()
        ism = data.get("ism")
        xabar = data['xabar']
        dasturlash = data.get('coder')
        companiya = data.get('companiya')
        await bot.send_message(chat_id=admin, text=f"Ism: {ism}\nxabar: {xabar}\ndasturlash tili: {dasturlash}\nIsh joyi: {companiya}\n")
        await bot.send_message(chat_id=kanal_id, text=f"Ism: {ism}\nxabar: {xabar}\ndasturlash tili: {dasturlash}\nIsh joyi: {companiya}\n")
        await call.answer("Adminga malumotlaringiz yuborildi", show_alert=True)
        await state.clear()
    else:
        await call.message.answer(f"Siz qaytadan royhatdan oting\nIsmingizni kiriting ?")
        await state.set_state(UserList.name)
         



async def main():
    await bot.send_message(chat_id=admin, text="Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Tugadi")
