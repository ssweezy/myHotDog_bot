from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from admin.requests import get_employees


adm_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сотрудники", callback_data="employees")],
    [InlineKeyboardButton(text="Сделать Рассылку", callback_data="mail")]])


control_employee = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начислить бонусы сотруднику', callback_data='send_bonus')],
    [InlineKeyboardButton(text='Списать бонусы с сотрудника', callback_data='take_back_bonus')]])


async def get_all_employees():
    all_employees = await get_employees()
    kbrd = []
    for employee in all_employees:
        kbrd.append([KeyboardButton(text=f'{employee.name} {employee.surname}')])
    kbrd1 = ReplyKeyboardMarkup(keyboard = kbrd, resize_keyboard=True, input_field_placeholder='Выбрать сотрудника')
    return kbrd1