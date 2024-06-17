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
    show_emp = State()
    cabinet = State()
    points = State()


# для отправки баллов
class ChooseEmpSendPoints(StatesGroup):
    Ask_points_amount = State()
    Points_amount = State()
    Msg_with_points = State()
    Acceptation = State()


# для отправки баллов
class ChooseEmpTakePoints(StatesGroup):
    Ask_points_amount = State()
    Points_amount = State()
    Msg_with_points = State()
    Acceptation = State()


# для отправления личного сообщения сотруднику
class SendMsgToEmp(StatesGroup):
    msg_to_send = State()


# для рассылки
class SendMsgToAllEmp(StatesGroup):
    msg_to_send = State()


# для настройки обучения
class Learning(StatesGroup):
    GetVideo = State()
