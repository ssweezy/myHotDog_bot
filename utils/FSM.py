from aiogram.fsm.state import State, StatesGroup


# для регистрации
class Reg(StatesGroup):
    password = State()
    name = State()
    surname = State()
    birthday = State()
    phoneNum = State()
    role = State()


# для меню
class Menu(StatesGroup):
    emp_menu = State()
    adm_menu = State()
    cabinet = State()
    points = State()



class Employee(StatesGroup):
    full_name = State()