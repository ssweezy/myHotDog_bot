from aiogram.types import Message
from aiogram import Router


router = Router()

# удаляет не значащие сообщения
@router.message()
async def del_trash(message: Message):
    await message.delete()