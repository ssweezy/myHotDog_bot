from time import sleep
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from utils.FSM import Choose_emp
from utils.database.requests import get_user_info, update_user_points
from utils.kb.inline_kb import control_employee, all_emp_kb, acceptation_points


router = Router()


# вывод всех сотрудников
@router.callback_query(F.data == "employees")
async def catalog(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
    await state.set_state(Choose_emp.Emp)
    await call.answer()


# обработка и вывод инфы по юзеру опираясь на коллбек(в нем юзер айди)
@router.callback_query(Choose_emp.Emp)
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


# запрос количества баллов для зачисления сотруднику CALLBACK
@router.callback_query(F.data == 'send_bonus')
async def ask_points_amount(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Сколько баллов <b>начислить</b> сотруднику?")
    print(call.message.message_id)
    await state.set_state(Choose_emp.Points_amount)
    await call.answer()


# сохраняет количество баллов и спрашивает за что начисление
@router.message(Choose_emp.Points_amount)
async def ask_msg_with_points(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    # проверка отправлено число или текст
    try:
        int(message.text)
        await state.update_data(points_to_send=message.text)
        await bot.edit_message_text(text="Напишите, за что начисляются баллы:",
                                    chat_id=data["chat_id"],
                                    message_id=data["msg_id"])
        await message.delete()
        await state.set_state(Choose_emp.Msg_with_points)
        print("прошел все")
    except:
        # если управляющий ввел не число, то его просит заново написать число

        await bot.edit_message_text(text="Введите число!",
                                    chat_id=data["chat_id"],
                                    message_id=data["msg_id"])
        await message.delete()
        await state.set_state(Choose_emp.Points_amount)


# подтверждение информации для зачисления баллов
@router.message(Choose_emp.Msg_with_points)
async def ask_msg_with_points(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(msg_to_send_with_points=message.text)
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(text=f"Кол-во начисляемых баллов: {data["points_to_send_amount"]}"
                                     f"\nЗа что начисляются: \n<i>{data["msg_to_send_with_points"]}</i>"
                                     f"\n\nВсе верно?",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"],
                                reply_markup=acceptation_points)
    await state.set_state(Choose_emp.Acceptation)


# обработка да или нет
@router.callback_query(Choose_emp.Acceptation)
async def send_or_not(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    user = await get_user_info(call.from_user.id)

    # обработка при нажатии да
    if call.data == "yes_p":
        # <================ДОДЕЛАТЬ СИСТЕМУ ОТПРАВКИ СООБЩЕНИЙ С БАЛЛАМИ
        await update_user_points(call.from_user.id, data["points_to_send"])
        await bot.send_message(text=f"Вам начислено <b>{data["points_to_send"]}</b>"
                                    f"\n<blockquote>{data["msg_to_send_with_points"]}</blockquote>",
                               chat_id=user.chat_id)

    # обработка при нажатии нет
    elif call.data == "no_p":
        await call.message.edit_text("<b>Отмена отправки.</b>")
        await call.message.edit_text("<b>Отмена отправки..</b>")
        await call.message.edit_text("<b>Отмена отправки...</b>")
        sleep(1)
        await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
        await state.set_state(Choose_emp.Emp)


@router.message(F.text == 'take_back_bonus')
async def catalog(message: Message, bot: Bot):
    msg = await message.answer('Зачем')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)