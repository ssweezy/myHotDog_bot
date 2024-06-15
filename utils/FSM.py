from aiogram.fsm.state import State, StatesGroup


# для регистрации
class Reg(StatesGroup):
    password = State()
    name = State()
    surname = State()
    birthday = State()
    phoneNum = State()
    role = State()
    acceptation = State()


# для меню
class Menu(StatesGroup):
    emp_menu = State()
    adm_menu = State()
    cabinet = State()
    points = State()



class Choose_emp(StatesGroup):
    Emp = State()
    Ask_points_amount = State()
    Points_amount = State()
    Msg_with_points = State()
    Acceptation = State()