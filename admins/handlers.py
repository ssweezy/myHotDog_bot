from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from utils.FSM import Employee, mail_state
from utils.kb.reply_kb import get_all_employees
from utils.kb.inline_kb import control_employee
from utils.database.requests import get_all_ID

router = Router()


# Список сотрудников
@router.callback_query(F.data == "employees")
async def catalog(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Employee.full_name)
    msg = await call.message.answer('Выберите сотрудника', reply_markup= await get_all_employees())
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)


@router.message(Employee.full_name)
async def emplfulnm(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    msg = await message.answer(f'Сотрудник: {data["full_name"]}', reply_markup = control_employee)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-2)
    await state.clear()


# Отправить бонусы сотруднику
@router.message(F.text == 'send_bonus')
async def send_bonus(message: Message, bot: Bot):
    msg = await message.answer('Как каиф')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)


# Списать бонусы у сотрудника
@router.message(F.text == 'take_back_bonus')
async def catalog(message: Message, bot: Bot):
    msg = await message.answer('Зачем')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)


# Написать рассылку
@router.callback_query(F.data == "mail")
async def catalog(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Напишите сообшение всем сотрудникам: ')
    await state.set_state(mail_state.msg)


# Рассылка
@router.message(mail_state.msg)
async def mail(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(msg=message.text)
    data = await get_all_ID()
    for empl in data:
        bot.send_message(text=message.text,chat_id=empl.tg_id)
    await message.answer('все, to be continued, сделать эту тему редактированной от прошлых сообщений')