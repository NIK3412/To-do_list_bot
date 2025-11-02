import asyncio
from aiogram import Bot, Dispatcher
from database.db import init_db
from handlers import start, notes
from config import TOKEN



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    init_db() #Запуск БД
    
    dp.include_router(start.router)
    dp.include_router(notes.router)
    print("Бот запущен")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
