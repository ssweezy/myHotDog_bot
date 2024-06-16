from time import sleep
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from utils.FSM import Menu
from utils.database.requests import get_user_info, update_user_points
from utils.kb.inline_kb import control_employee, all_emp_kb, acceptation_points, adm_menu_kb


router = Router()


# вывод всех сотрудников
@router.callback_query(F.data == "employees")
async def catalog(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
    await state.set_state(Menu.show_emp)
    await call.answer()


# обработка и вывод инфы по юзеру опираясь на коллбек(в нем юзер айди)
@router.callback_query(Menu.show_emp)
async def show_user_info(call: CallbackQuery, state: FSMContext):
    user = (await get_user_info(call.data))
    # присваивание айди юзера в data чтобы можно было дальше с ним работать
    await state.update_data(choose_emp_id=call.data)
    await call.message.edit_text("Информация по сотруднику:"
                                 f"\nФИ - {user.name} {user.surname}"
                                 f"\nТелеграм юзернейм - {user.tg_username}"
                                 f"\nРоль - {user.role}"
                                 f"\nДата регистрации в бот - {user.reg_date}"
                                 f"\nБаллы - <b>{user.points}</b>", reply_markup=control_employee)
    await call.answer()
    await state.set_state(None)


@router.message(F.text == 'take_back_points')
async def catalog(message: Message, bot: Bot):
    msg = await message.answer('Зачем')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)