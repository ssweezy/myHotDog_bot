from aiogram.fsm.state import State, StatesGroup


class Reg(StatesGroup):
    password = State()
    name = State()
    surname = State()
    birthday = State()
    phoneNum = State()
    role = State()


class Menu(StatesGroup):
    emp_menu = State()
    adm_menu = State()
    cabinet = State()
    points = State()