
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from keyboards import Inline_keyboard
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext



router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет 👋 Я бот для заметок\n"
                         "/add - добавить заметку\n"
                         "/list - список заметок\n"
                         "/delete - удалить по ID\n"
                         "/cross - зачеркнуть заметку", reply_markup=Inline_keyboard())
    state.clear()