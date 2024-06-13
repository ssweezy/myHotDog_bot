from aiogram.fsm.state import State, StatesGroup


class Reg(StatesGroup):
    password = State()
    name = State()
    surname = State()
    phoneNum = State()
    role = State()


class Regular(StatesGroup):
    menu = State()