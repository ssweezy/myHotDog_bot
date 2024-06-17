from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from utils.FSM import Menu
from utils.database.requests import get_user_info
from utils.kb.inline_kb import control_employee, all_emp_kb


router = Router()


# вывод всех сотрудников
@router.callback_query(F.data == "employees")
async def catalog(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
    await state.set_state(Menu.show_emp)
    await call.answer()


# обработка и вывод инфы по юзеру опираясь на коллбек(в нем юзер айди)
@router.callback_query(Menu.show_emp)
async def show_user_info(call: CallbackQuery, state: FSMContext):
    user = (await get_user_info(call.data))
    # присваивание айди юзера в data чтобы можно было дальше с ним работать
    await state.update_data(choose_emp_id=call.data)
    await call.message.edit_text("<b>Информация по сотруднику:</b>"
                                 f"\n\nФИ - {user.name} {user.surname}"
                                 f"\nТелеграм юзернейм - {user.tg_username}"
                                 f"\nРоль - {user.role}"
                                 f"\nДата регистрации в бот - {user.reg_date}"
                                 f"\nБаллы - <b>{user.points}</b>", reply_markup=control_employee)
    await call.answer()
    await state.set_state(None)

