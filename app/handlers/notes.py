from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from database.db import add_note, delete_notes, get_notes, done_task
import datetime

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
    
    
    """Функция вывода заметок"""
@router.message(Command(commands=["list"]))
async def get_n(message: types.Message):
    notes = get_notes(message.from_user.id)
    if not notes:
        await message.answer("У вас еще нет заметок, вы можете их добавить с помощью /add #Текст заметки")
        return
    text = ""
    for note in notes:
        print(f"\n{note}")
        if note['is_done']:
            text += f"<s>{note['note_id']} {note['text']}</s>        {note['da_te'].strftime("%Y-%m-%d %H:%M")}✅\n"
        else:
            text += f"{note['note_id']} {note['text']}            {note['da_te'].strftime("%Y-%m-%d %H:%M")}\n"       
        
    await message.answer(f"📋 Ваши заметки:\n{text}",parse_mode='HTML')
    

'''Функция удаления заметки'''  
@router.message(Command(commands=["delete"]))
async def del_n(message: types.Message):
    args = message.text.replace("/delete", "").strip()
    if not args.isdigit():
        await message.answer("Укажи ID заметки, например: /delete 2")
        return
    note_id = int(args)
    delete_notes(message.from_user.id, note_id)
    await message.answer(f'Заметка {note_id} была удалена')

@router.message(Command(commands=("cross")))
async def cross(message: types.Message):
    args = message.text.replace("/cross", "").strip()
    if not args.isdigit():
        await message.answer('введите номер заметки которую хотите удалить')
        return
    note_id = int(args)
    crossed_note = done_task(message.from_user.id, note_id)
    if not crossed_note:
        await message.answer("❌ Такой заметки не существует")
        return
    is_done, text = crossed_note['is_done'], crossed_note['text']

    if is_done:
        await message.answer(f"✅ Заметка '{text}' зачёркнута")
    else:
        await message.answer(f" Зачёркивание снято с заметки '{text}'")

    