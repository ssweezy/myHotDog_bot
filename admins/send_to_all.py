from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils.database.requests import get_employees
from utils.FSM import SendMsgToAllEmp, Menu
from utils.kb.inline_kb import back_kb, acceptation_msg_all, all_emp_kb

router = Router()


# запрос сообщения для отправления рассылки
@router.callback_query(F.data == "mail")
async def asking_msg_for_all(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>Напишите сообщение для рассылки</b>", reply_markup=back_kb)
    await state.set_state(SendMsgToAllEmp.msg_to_send)


# подтверждение отправки сообщения рассылки
@router.message(SendMsgToAllEmp.msg_to_send)
async def confirm_sending(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.update_data(msg_to_all=message.text)  # сохранение сообщения в data
    await bot.edit_message_text(text=f"<b>Ваше сообщение для рассылки:</b>"
                                     f"\n<blockquote>{message.text}</blockquote>",
                                chat_id=data["chat_id"],
                                message_id=data["msg_id"],
                                reply_markup=acceptation_msg_all)
    await message.delete()


# обработка callback "yes_a", отправка рассылки
@router.callback_query(F.data == "yes_a")
async def sending_msg_all(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    for emp in (await get_employees()):
        await bot.send_message(text=f"Сообщение от управляющего:"
                                    f"\n<blockquote>{data["msg_to_all"]}</blockquote>",
                               chat_id=emp.chat_id)
    await call.message.edit_text("<b>Рассылка завершена✔️</b>")
    sleep(2)
    await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
    await state.set_state(Menu.show_emp)


# реакция на callback no_a, отмена отправки рассылки
@router.callback_query(F.data == 'no_a')
async def cancel_sending_msg(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>Отмена отправки.</b>")
    sleep(0.5)
    await call.message.edit_text("<b>Отмена отправки..</b>")
    sleep(0.5)
    await call.message.edit_text("<b>Отмена отправки...</b>")
    sleep(0.5)
    await call.message.edit_text("Выберите сотрудника:", reply_markup=await all_emp_kb())
    await state.set_state(Menu.show_emp)
