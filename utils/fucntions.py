from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.database.requests import get_user_info
from utils.kb.inline_kb import emp_menu_kb, adm_menu_kb


# данный файл хранит в себе функции для общего использования


router = Router()


# функция для обновления данных в data, это сделано для того чтобы можно в любой момент обновить данные в любой функции
async def update_data(user_id, chat_id, state):
    user = await get_user_info(user_id)
    await state.update_data(tg_id=user.tg_id)
    await state.update_data(tg_username=user.tg_username)
    await state.update_data(role=user.role)
    await state.update_data(category=user.category)
    await state.update_data(name=user.name)
    await state.update_data(surname=user.surname)
    await state.update_data(birthday=user.birthday)
    await state.update_data(phone=user.phone)
    await state.update_data(msg_id=user.msg_id)
    await state.update_data(chat_id=chat_id)


# функция для обработки нажатия на кнопку "назад"
@router.callback_query(F.data == "back")
async def func_back(call: CallbackQuery, state: FSMContext, bot: Bot):
    await update_data(call.from_user.id, call.message.chat.id, state)
    data = await state.get_data()
    if data["category"] == "emp":
        await call.message.edit_text('<b>МЕНЮ</b>', reply_markup=emp_menu_kb)
        await state.set_state(None)
    else:
        # удаление видео при замене видео, learning_settings line ~24, используется данная конструкция потому что видео
        # не всегда существует в чате и попытка его удаления вызовет ошибку
        try:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=data["video_id"])
        except:
            pass
        await call.message.edit_text(f"<b>В вашем распоряжении следующие функции</b>", reply_markup=adm_menu_kb)
        await state.set_state(None)


# удаляет не значащие сообщения
@router.message()
async def del_trash(message: Message):
    await message.delete()