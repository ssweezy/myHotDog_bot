from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from utils.database.requests import get_employees





async def get_all_employees():
    all_employees = await get_employees()
    kbrd = []
    for employee in all_employees:
        kbrd.append([KeyboardButton(text=f'{employee.name} {employee.surname}')])
    kbrd1 = ReplyKeyboardMarkup(keyboard = kbrd, resize_keyboard=True, input_field_placeholder='Выбрать сотрудника')
    return kbrd1