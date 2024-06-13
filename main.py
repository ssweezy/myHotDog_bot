import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from utils.config import TOKEN
from utils.database.models import async_main

from employee.reg import router


async def main():
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')