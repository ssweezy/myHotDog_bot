from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils.database.requests import update_file_id, get_file_id
from utils.kb.inline_kb import learn_settings_kb, back_kb, adm_menu_kb
from utils.FSM import Learning

router = Router()


# вывод доступных настроек для видео
@router.callback_query(F.data == "change_learn")
async def settings_menu(call: CallbackQuery):
    await call.message.edit_text("<b>Настройки обучения:</b>", reply_markup=learn_settings_kb)


# сохранение номера видео
@router.callback_query(F.data.startswith("replace"))
async def save_video_num(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Перед вами текущее видео\n\n<b>Пришлите нужное видео</b>', reply_markup=back_kb)
    # отправка текущего видео
    video = await call.message.answer_video(video=await get_file_id(int(call.data[-1])))
    await state.update_data(video_id=video.message_id)  # сохранение айди видео чтобы потом удалить его
    await state.set_state(Learning.GetVideo)
    await state.update_data(video_num=int(call.data[-1]))


# сохранение file_id и замена выбранного видео
@router.message(Learning.GetVideo)
async def replace_video(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    file_id = message.video.file_id  # получение file_id
    await update_file_id(data["video_num"], file_id)  # сохранение file_id в бд
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=data["video_id"])  # удаление видео, отправленное ботом
    await bot.edit_message_text(text='<b>Видео успешно заменено!</b>',
                                chat_id=data["chat_id"],
                                message_id=data["msg_id"])
    sleep(2)
    # возвращение в админскому меню
    await bot.edit_message_text(f"<b>В вашем распоряжении следующие функции</b>",
                                chat_id=data["chat_id"],
                                message_id=data["msg_id"],
                                reply_markup=adm_menu_kb)
    await state.set_state(None)




