from aiogram import Router
from aiogram.types import Message

from utils.database.requests import get_user_info

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


# удаляет не значащие сообщения
@router.message()
async def del_trash(message: Message):
    await message.delete()