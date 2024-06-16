import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from utils.config import TOKEN
from utils.database.models import async_main

from employee.reg import router as r1
from employee.emp_menu import router as r2
from admins.adm_menu import router as r3
from admins.send_points import router as r4
from admins.take_back_points import router as r5
from admins.send_msg import router as r6
from admins.send_to_all import router as r7
from admins.rating import router as r8
# импортировать роутер из functions


async def main():
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(r1, r2, r3, r4, r5, r6, r7, r8)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        print("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')