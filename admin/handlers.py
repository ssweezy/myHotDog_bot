from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import admin.keyboards as kb

router = Router()


class Employee(StatesGroup):
    full_name = State()


@router.message(Command('test'))
async def test(message: Message, bot: Bot):
    msg = await message.answer('Добро пожаловать, {имя}!', reply_markup = kb.main)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)


@router.message(F.text == 'Сотрудники')
async def catalog(message: Message, bot: Bot, state: FSMContext):
    msg = await message.answer('Выбери сотрудника', reply_markup= await kb.get_all_employees())
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-2)
    await state.set_state(Employee.full_name)


@router.message(Employee.full_name)
async def emplfulnm(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    msg = await message.answer(f'Сотрудник: {data["full_name"]}', reply_markup = kb.control_employee)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-2)
    await state.clear()


@router.message(F.text == 'Начислить бонусы сотруднику')
async def send_bonus(message: Message, bot: Bot):
    msg = await message.answer('Как каиф')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)


@router.message(F.text == 'Списать бонусы с сотрудника')
async def catalog(message: Message, bot: Bot):
    msg = await message.answer('Зачем')
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-1)