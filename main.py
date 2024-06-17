import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils.config import TOKEN
from utils.database.models import async_main


from utils.fucntions import router as r1  # добавлять в dp_include самым последним, потому что содержит функцию
# del_trash, если импортировать не последним, то вызывает ошибки в работе бота
from utils.reg import router as r2
from employee.learning import router as r3
from employee.cabinet import router as r4
from admins.actions_with_emp.emp_list import router as r5
from admins.actions_with_emp.send_points import router as r6
from admins.actions_with_emp.take_back_points import router as r7
from admins.actions_with_emp.send_msg import router as r8
from admins.send_to_all import router as r9
from admins.rating import router as r10
from admins.actions_settings.settings import router as r11
from admins.actions_settings.learning_settings import router as r12


async def main():
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r1)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        print("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')