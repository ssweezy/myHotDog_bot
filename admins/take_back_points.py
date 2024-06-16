from time import sleep
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from utils.FSM import ChooseEmpTakePoints, Menu
from utils.database.requests import get_user_info, update_user_points
from utils.kb.inline_kb import control_employee, all_emp_kb, acceptation_points, adm_menu_kb


router = Router()


@router.callback_query(F.data == 'take_back_points')
async def ask_points_amount(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Сколько баллов <b>списать</b> у сотрудника?")
    await state.set_state(ChooseEmpTakePoints.Points_amount)
    await call.answer()


# сохраняет количество баллов и спрашивает за что начисление
@router.message(ChooseEmpTakePoints.Points_amount)
async def ask_msg_with_points(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    # проверка отправлено число или текст
    try:
        int(message.text)
        await state.update_data(points_to_send=message.text)
        await bot.edit_message_text(text="Напишите, за что <b>списываются</b> баллы:",
                                    chat_id=data["chat_id"],
                                    message_id=data["msg_id"])
        await message.delete()
        await state.set_state(ChooseEmpTakePoints.Msg_with_points)
    except:
        # если управляющий ввел не число, то его просит заново написать число

        await bot.edit_message_text(text="Введите число!",
                                    chat_id=data["chat_id"],
                                    message_id=data["msg_id"])
        await message.delete()
        await state.set_state(ChooseEmpTakePoints.Points_amount)


# подтверждение информации для зачисления баллов
@router.message(ChooseEmpTakePoints.Msg_with_points)
async def ask_msg_with_points(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(msg_to_send_with_points=message.text)
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(text=f"Кол-во списываемых баллов: {data["points_to_send"]}"
                                     f"\nПричина списания: \n<blockquote>{data["msg_to_send_with_points"]}</blockquote>"
                                     f"\n\nВсе верно?",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"],
                                reply_markup=acceptation_points)
    await state.set_state(ChooseEmpTakePoints.Acceptation)


# отправка баллов или отмена отправки, если отмена то возвращает меню выбора сотрудника
@router.callback_query(ChooseEmpTakePoints.Acceptation)
async def send_or_not(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    user = await get_user_info(data["choose_emp_id"])

    # обработка при нажатии да
    if call.data == "yes_p":
        # <================ДОДЕЛАТЬ СИСТЕМУ ОТПРАВКИ СООБЩЕНИЙ С БАЛЛАМИ
        await update_user_points(data["choose_emp_id"], (user.points - int(data["points_to_send"])))
        points = [i for i in str(data["points_to_send"])]

        # проверка для подставления правильного склонения слова "баллов" или балла
        if ((int(points[-1]) == 0 or int(points[-1]) > 4) and int("".join(points)) < 21) or (int(points[-1]) > 4 or int(points[-1]) == 0):
            await bot.send_message(text=f"У вас списалось <b>{data["points_to_send"]} баллов</b>"
                                        f"\n<blockquote>{data["msg_to_send_with_points"]}</blockquote>",
                                        chat_id=user.chat_id)
        else:
            await bot.send_message(text=f"У вас списалось <b>{data["points_to_send"]} балла</b>"
                                        f"\n<blockquote>{data["msg_to_send_with_points"]}</blockquote>",
                                   chat_id=user.chat_id)
        await call.message.edit_text("<b>Баллы успешно списаны!</b>")  # информация об успешном зачислении
        sleep(2)
        # возвращение обычного меню
        await call.message.edit_text("<b>В вашем распоряжении следующие функции</b>", reply_markup=adm_menu_kb)
        await state.set_state(Menu.show_emp)

    # обработка при нажатии нет
    elif call.data == "no_p":
        await call.message.edit_text("<b>Отмена списания.</b>")
        sleep(0.5)
        await call.message.edit_text("<b>Отмена списания..</b>")
        sleep(0.5)
        await call.message.edit_text("<b>Отмена списания...</b>")
        sleep(0.5)
        await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
        await state.set_state(Menu.show_emp)