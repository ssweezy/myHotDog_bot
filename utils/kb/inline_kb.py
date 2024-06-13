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


# клавиатура для меню админов *доделать
adm_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мой кабинет", callback_data="cabinet")],
    [InlineKeyboardButton(text="За что начисляем баллы?", url="https://telegra.ph/MYHOTDOG-Bally-06-13")],
    [InlineKeyboardButton(text="Проверить свои баллы", callback_data="check_points")]
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










