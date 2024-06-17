from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils.kb.inline_kb import settings_kb

router = Router()


# вывод доступных настроек
@router.callback_query(F.data == "settings")
async def settings_menu(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>Доступны следующие настройки:</b>", reply_markup=settings_kb)




