from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.FSM import Menu


# в этом файле будет проходить вся обработка кнопок в меню

# меню появляется в том же сообщении, где проходила регистрация, к этому сообщению прикрепляется меню в зависимости от
# категории пользователя| reg.py line ~190


router = Router()


@router.callback_query(F.data == 'cabinet')
async def button_cabinet(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()

