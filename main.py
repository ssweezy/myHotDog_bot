import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from utils.config import TOKEN
from utils.database.models import async_main


from employee.reg import router as r1
from employee.emp_menu import router as r2
from admins.handlers import router as r3
from utils.delete_unwanted_msg import router as r4


async def main():
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(r1, r2, r3, r4)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        print("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')