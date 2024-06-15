from time import sleep
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from utils.FSM import Choose_emp
from utils.database.requests import get_user_info
from utils.kb.inline_kb import control_employee, all_emp_kb, acceptation


router = Router()


# вывод всех сотрудников
@router.callback_query(F.data == "employees")
async def catalog(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
    await state.set_state(Choose_emp.Emp)


# обработка и вывод инфы по юзеру опираясь на коллбек(в нем юзер айди)
@router.callback_query(Choose_emp.Emp)
async def show_user_info(call:CallbackQuery, state: FSMContext):
    user = await get_user_info(call.data)
    # присваивание айди юзера в data чтобы можно было дальше с ним работать
    await state.update_data(choose_emp_id=call.data)
    await call.message.edit_text("Информация по сотруднику:"
                                 f"\nФИ - {user.name} {user.surname}"
                                 f"\nТелеграм юзернейм - {user.tg_username}"
                                 f"\nРоль - {user.role}"
                                 f"\nДата регистрации в бот - {user.reg_date}"
                                 f"\nБаллы - <b>{user.points}</b>", reply_markup=control_employee)


# запрос количества баллов для зачисления сотруднику
@router.callback_query(F.data == 'send_bonus' or Choose_emp.Ask_points_amount)
async def ask_points_amount(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Сколько баллов <начислить> сотруднику?")
    await state.set_state(Choose_emp.Points_amount)


# сохраняет количество баллов и спрашивает за что начисление
@router.message(Choose_emp.Points_amount)
async def ask_msg_with_points(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await message.delete()
    # проверка отправлено число или текст
    try:
        int(message.text)
        await state.update_data(points_to_send_amount=message.text)
        await bot.edit_message_text(text="Напишите, за что начисляются баллы:",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.set_state(Choose_emp.Msg_with_points)
    # если управляющий ввел не число, то его просит заново написать число
    except:
        await bot.edit_message_text(text="Введите число!",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.set_state(Choose_emp.Ask_points_amount)


# подтверждение информации для зачисления баллов
@router.message(Choose_emp.Msg_with_points)
async def ask_msg_with_points(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(msg_to_send_with_points=message.text)
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(text=f"Количество начисляемых баллов - {data["points_to_send_amount"]}"
                                     f"\nЗа что начисляются - <i>{data["msg_to_send_with_points"]}</i>"
                                     f"\n\nВсе верно?",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"],
                                reply_markup=acceptation)
    await state.set_state(Choose_emp.Acceptation)


# обработка да или нет
@router.callback_query(Choose_emp.Acceptation)
async def send_or_not(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == "yes":
        pass  # <================ДОДЕЛАТЬ СИСТЕМУ ОТПРАВКИ СООБЩЕНИЙ С БАЛЛАМИ
    elif call.data == "no":
        await call.message.edit_text("<b>Отмена отправка...</b>")
        sleep(3)
        await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
        await state.set_state(Choose_emp.Emp)


@router.message(F.text == 'take_back_bonus')
async def catalog(message: Message, bot: Bot):
    msg = await message.answer('Зачем')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)