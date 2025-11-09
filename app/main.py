import asyncio
from aiogram import Bot, Dispatcher
from database.db import init_db
from handlers import start, notes
from config import TOKEN
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):

    await bot.delete_my_commands(scope=BotCommandScopeDefault())

    commands = [
        BotCommand(command="start", description="стартовое меню"),
        BotCommand(command="list", description="список заметок"),
        BotCommand(command="delete", description="удалить"),
        BotCommand(command="cross", description="перечеркнуть"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    init_db() #Запуск БД
    dp.include_router(start.router)
    dp.include_router(notes.router)
    print("Бот запущен")
    commands = await bot.get_my_commands()
    print(commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
