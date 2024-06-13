from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

from admin.requests import get_employees


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Сотрудники'),
                                      KeyboardButton(text='Сделать Рассылку')]],
                            resize_keyboard=True,
                            input_field_placeholder='Выбрать действие')


control_employee = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начислить бонусы сотруднику'),
                                                  KeyboardButton(text='Списать бонусы с сотрудника')]],
                                        resize_keyboard=True,
                                        input_field_placeholder='Выбрать действие')


async def get_all_employees():
    all_employees = await get_employees()
    kbrd = []
    for employee in all_employees:
        kbrd.append([KeyboardButton(text=f'{employee.name} {employee.surname}')])
    kbrd1 = ReplyKeyboardMarkup(keyboard = kbrd, resize_keyboard=True, input_field_placeholder='Выбрать сотрудника')
    return kbrd1