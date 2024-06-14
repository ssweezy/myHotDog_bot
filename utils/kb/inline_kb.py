from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
    [InlineKeyboardButton(text="Сделать Рассылку", callback_data="mail")]])


# начисление баллов сотрудникам
control_employee = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начислить бонусы сотруднику', callback_data='send_bonus')],
    [InlineKeyboardButton(text='Списать бонусы с сотрудника', callback_data='take_back_bonus')]])






