import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db.database import init_db
from src.handlers import router as handlers_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    init_db()
    dp.include_router(router=handlers_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())