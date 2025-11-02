from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from database.db import add_note, delete_notes, get_notes
router = Router()

'''функция создания заметки'''
@router.message(Command(commands=["add"]))
async def add_n(message: types.Message): 
    repl = message.text.replace("/add", "").strip()
    if not repl:
        await message.answer("Введите тект заметки")
        return
    
    add_note(message.from_user.id, repl)
    
    await message.answer("✅ Заметка добавлена!")
    
@router.message(Command(commands=["list"]))
async def get_n(message: types.Message):
    notes = get_notes(message.from_user.id)
    if not notes:
        await message.answer("У вас еще нет заметок, вы можете их добавить с помощью /add #Текст заметки")
        return
    text = "\n".join([f"{note['id']}. {note['text']}" for note in notes])
    await message.answer(f"🔍 Найдено:\n{text}")
    
@router.message(Command(commands=["delete"]))
async def del_n(message: types.Message):
    args = message.text.replace("/delete", "").strip()
    if not args.isdigit():
        await message.answer("Укажи ID заметки, например: /delete 2")
        return
    note_id = int(args)
    delete_notes(message.from_user.id, note_id)
    await message.answer(f'Заметка {note_id} была удалена')