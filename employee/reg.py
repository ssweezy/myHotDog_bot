from time import sleep
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.database.requests import set_user, user_exists, get_user_info
from utils.FSM import Reg
from utils.config import PASSWORD, PASSWORD_ADMIN
from utils.kb.inline_kb import acceptation, emp_menu_kb, adm_menu_kb

router = Router()


# приветствие и запрос пароля
@router.message(Command('start'))
async def hello(message: Message, bot: Bot, state: FSMContext):
    # проверка если есть юзер то команда старт не будет работать
    if not (await user_exists(message.from_user.id)):
        await message.answer(f"👋 Приветствуем {message.from_user.username}!")
        msg = await message.answer("🔐 Для регистрации вам необходимо ввести код-пароль.\nВведите пароль:")
        await state.update_data(msg_id=msg.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id - 2)
        await state.set_state(Reg.password)
    else:
        # проверка если есть юзер то отправить его на соответсвующее меню
        user_data = await get_user_info(message.from_user.id)
        if(user_data.category=='adm'):
            msg = await message.answer(f"<b>В вашем распоряжении следующие функции</b>", reply_markup=adm_menu_kb)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 2)
        elif(user_data.category=='emp'): 
            msg = await message.answer(f"<b>МЕНЮ</b>", reply_markup=emp_menu_kb)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 2)
        else:
            await message.answer('У вас нет роли')
        await message.delete()


# проверка пароля или старт если человек зареган
@router.message(Reg.password)
async def pass_check(message: Message, bot: Bot, state: FSMContext):

    # регистрация для сотрудников
    if message.text == PASSWORD:
        data = await state.get_data()
        await message.delete()
        await bot.edit_message_text(text="🔓 Вы успешно вошли в систему!\nВведите <b>имя:</b>",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(tg_username=message.from_user.username)
        await state.update_data(role="")
        await state.update_data(category="emp")
        await state.set_state(Reg.name)

    # регистрация для админов
    elif message.text == PASSWORD_ADMIN:
        data = await state.get_data()
        await message.delete()
        await bot.edit_message_text(text="🔓 Вы успешно вошли в систему как <b>управляющий</b>!\nВведите <b>имя:</b>",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(tg_username=message.from_user.username)
        await state.update_data(role="adm")
        await state.update_data(category="adm")
        await state.set_state(Reg.name)

    # неправильный пароль
    else:
        await message.delete()
        data = await state.get_data()
        try:
            await bot.edit_message_text(text="🔒 <b>Неверный пароль</b>\nПопробуйте еще раз:", chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        except:
            pass


# имя
@router.message(Reg.name)
async def get_name(message: Message, bot: Bot ,state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nВведите <b>фамилию:</b>", chat_id=message.chat.id,
                                message_id=data["msg_id"])
    await state.set_state(Reg.surname)


# фамилия
@router.message(Reg.surname)
async def get_surname(message: Message, bot: Bot ,state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nФамилия - {data["surname"]}"
                                     f"\nВведите <b>дату рождения:</b>", chat_id=message.chat.id,
                                message_id=data["msg_id"])
    await state.set_state(Reg.birthday)


# день рождения
@router.message(Reg.birthday)
async def get_birthday(message: Message, bot: Bot ,state: FSMContext):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nФамилия - {data["surname"]}"
                                     f"\nДата рождения - {data["birthday"]}"
                                     f"\nВведите <b>номер телефона:</b>", chat_id=message.chat.id,
                                message_id=data["msg_id"])
    await state.set_state(Reg.phoneNum)


# номер телефона
@router.message(Reg.phoneNum)
async def get_phone(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.delete()

    # если пользователь, то ему нужно вводить свою роль
    if data["category"] == 'emp':
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                         f"\nИмя - {data["name"]}"
                                         f"\nФамилия - {data["surname"]}"
                                         f"\nДата рождения - {data["birthday"]}"
                                         f"\nТелефон - {data["phone"]}"
                                         f"\nВведите <b>свою роль</b>", chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.set_state(Reg.role)

    # если пользователь админ, то ему не нужно указывать свою роль, смотрите line 52
    else:
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                         f"\nИмя - {data["name"]}"
                                         f"\nФамилия - {data["surname"]}"
                                         f"\nДата рождения - {data["birthday"]}"
                                         f"\nТелефон - {data["phone"]}"
                                         f"\n\n<b>Все верно?</b>", chat_id=message.chat.id,
                                    message_id=data["msg_id"], reply_markup=acceptation)


# роль пользователя
@router.message(Reg.role)
async def get_role(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data["role"] != "":
        await message.delete()
    else:
        await state.update_data(role=message.text)
        data = await state.get_data()
        await message.delete()
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nФамилия - {data["surname"]}"
                                     f"\nДата рождения - {data["birthday"]}"
                                     f"\nТелефон - {data["phone"]}"
                                     f"\nРоль - {data["role"]}"
                                     f"\n\n<b>Все верно?</b>", chat_id=message.chat.id,
                                message_id=data["msg_id"], reply_markup=acceptation)


# кнопка "Да"
@router.callback_query(F.data == 'yes')
async def reg_db(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    print(call.from_user)
    info = [call.from_user.id,
            call.from_user.username,
            data["role"],
            data["category"],
            data["name"],
            data["surname"],
            data["birthday"],
            data["phone"],
            str(datetime.now())[:19]
            ]
    # проверка на ошибку при регистрации, если она возникает, то регистрацию нужно пройти заново
    try:
        await set_user(info)
    except:
        category = (await state.get_data())["category"]
        await state.clear()
        if category == 'admin':
            await state.update_data(category=category)
            await state.update_data(role=category)
        else:
            await state.update_data(category=category)
        await call.message.edit_text(text="Возникла ошибка...Пройдите регистрацию заново\n<b>Введите имя</b>")
        await state.set_state(Reg.name)
        return

    await call.message.delete()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
    msg = await bot.send_message(text="Поздравляем! Вы теперь зарегистрированы!", chat_id=call.message.chat.id,
                           message_effect_id="5046509860389126442")
    await state.update_data(msg_id=msg.message_id) # перепривязка айди сообщения чтобы им было удобно управлять

    # фриз на 3 секунды, затем появляется меню, вид меню определяется в зависимости от категории пользователя
    sleep(3)
    if data["category"] == "emp":
        await bot.edit_message_text(text=f"<b>МЕНЮ</b>",
                                    chat_id=call.message.chat.id,
                                    message_id=msg.message_id,
                                    reply_markup=emp_menu_kb)
    else:
        await bot.edit_message_text(text=f"<b>В вашем распоряжении следующие функции</b>",
                                    chat_id=call.message.chat.id,
                                    message_id=msg.message_id,
                                    reply_markup=adm_menu_kb)
    await state.set_state(None)


# кнопка "Нет"
@router.callback_query(F.data == 'no')
async def reg_repeat(call: CallbackQuery, bot: Bot, state: FSMContext):
    category = (await state.get_data())["category"]
    await state.clear()
    # проверка админ или нет для правильного заполнения роли, иначе без этого выдает ошибку
    if category == 'admin':
        await state.update_data(category=category)
        await state.update_data(role=category)
    else:
        await state.update_data(category=category)
    await state.update_data(msg_id=call.message.message_id)
    await call.message.edit_text(text="Заполняем заново...\n<b>Введите имя</b>")
    await state.set_state(Reg.name)



