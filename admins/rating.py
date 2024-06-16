from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.database.requests import get_employees, get_user_info
from utils.kb.inline_kb import back_kb

router = Router()


# составление рейтинга сотрудников
@router.callback_query(F.data == "rating")
async def show_rating(call: CallbackQuery):
    users = await get_employees()
    # сортировка сотрудников по баллам
    rating_dict = {i.tg_id: i.points for i in users}
    rating_list = sorted(rating_dict.items(), key=lambda x: x[1], reverse=True)
    print(rating_list)
    text = "<B>РЕЙТИНГ СОТРУДНИКОВ</B>"
    # цикл вывода рейтинга
    for i in range(len(rating_list)):
        print(i)
        user = await get_user_info(rating_list[i][0])  # мы обрабатываем примерно -> [(1325339634, 5), (1244352262, 9)]
        text = text + f"\n\n<b>{i+1}</b>. {user.name}, баллы: {user.points}"

    await call.message.edit_text(text, reply_markup=back_kb)
    await call.answer()

