
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет 👋 Я бот для заметок.\nИспользуй команды:\n"
                         "/add — добавить заметку\n"
                         "/list — список заметок\n"
                         "/delete — удалить по ID")
