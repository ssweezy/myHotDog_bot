from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.database.requests import get_employees


# клавиатура для подтверждения корректности информации при регистрации
acceptation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes"),
     InlineKeyboardButton(text='Нет', callback_data='no')]
    ])


# клавиатура для меню сотрудников
emp_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мой кабинет", callback_data="cabinet")],
    [InlineKeyboardButton(text="За что начисляем баллы?", url="https://telegra.ph/MYHOTDOG-Bally-06-13")],
    [InlineKeyboardButton(text="Пройти обучение", callback_data="tutor")]
    ])


# кнопка для возвращения в предыдущее положение
back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# кнопка для возвращения в предыдущее положение
back_points_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")],
    [InlineKeyboardButton(text="Проверить свои баллы", callback_data="check_points")]
    ])


# ====================АДМИНСКАЯ ЧАСТЬ====================
# админская клавиатура
adm_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сотрудники", callback_data="employees")],
    [InlineKeyboardButton(text="Сделать Рассылку", callback_data="mail")],
    ])


# начисление баллов сотрудникам
control_employee = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начислить бонусы', callback_data='send_bonus')],
    [InlineKeyboardButton(text='Списать бонусы', callback_data='take_back_bonus')],
    [InlineKeyboardButton(text="Отправить сообщение сотруднику", callback_data="send_msg")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# вывод всех сотрудников, callback = айди юзера, это сделано чтобы можно было удобно доставать всю информацию о нем
async def all_emp_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад', callback_data="back"))
    for emp in await get_employees():
        kb.add(InlineKeyboardButton(text=f'{emp.name} {emp.surname}', callback_data=f"{emp.tg_id}"))
    return kb.as_markup()







