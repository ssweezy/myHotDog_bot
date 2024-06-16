from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from utils.kb.inline_kb import emp_menu_kb, back_kb, back_points_kb, adm_menu_kb
from utils.database.requests import get_points
from utils.fucntions import update_data

# в этом файле будет проходить вся обработка кнопок в меню

# меню появляется в том же сообщении, где проходила регистрация, к этому сообщению прикрепляется меню в зависимости от
# категории пользователя| reg.py line ~190


router = Router()


# переход в кабинет **функционал скудный какой-то, стоит что-то интересное придумать когда завершим работу над основой
@router.callback_query(F.data == 'cabinet')
async def button_cabinet(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await call.message.edit_text(text="<b>Ваш кабинет</b>\n"
                                      f"\nИмя - {data["name"]}"
                                      f"\nФамилия - {data["surname"]}"
                                      f"\nДата рождения - {data["birthday"]}"
                                      f"\nТелефон - {data["phone"]}"
                                      f"\nРоль - {data["role"]}",
                                 reply_markup=back_points_kb
                                 )


# проверка кол-ва баллов
@router.callback_query(F.data == "check_points")
async def check_points(call: CallbackQuery):
    points = await get_points(call.from_user.id)
    await call.message.edit_text(text=call.message.text+f"\nУ вас <b>{points}</b> баллов", reply_markup=back_kb)


# функция для обработки нажатия на кнопку "назад"
@router.callback_query(F.data == "back")
async def func_back(call: CallbackQuery, state: FSMContext):
    await update_data(call.from_user.id, call.message.chat.id, state)
    data = await state.get_data()
    if data["category"] == "emp":
        await call.message.edit_text('<b>МЕНЮ</b>', reply_markup=emp_menu_kb)
        await state.set_state(None)
    else:
        await call.message.edit_text(f"<b>В вашем распоряжении следующие функции</b>", reply_markup=adm_menu_kb)
        await state.set_state(None)


