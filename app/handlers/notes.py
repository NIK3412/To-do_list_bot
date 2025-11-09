from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from database.db import add_note, delete_notes, get_notes, done_task
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


router = Router()


#FSM
class index(StatesGroup):
    m_id = State()
    done = State()
    add = State()

'''функция создания заметки'''
@router.message(Command("add"))
async def add_note_cmd(message: Message, state: FSMContext):
    """Добавление заметки через команду /add [текст]"""
    text = message.text.replace("/add", "").strip()

    if not text:
        # Если пользователь не указал текст — переходим в FSM
        await state.set_state(index.add)
        await message.answer("Введите текст заметки:")
        return

    add_note(message.from_user.id, text)
    await message.answer("✅ Заметка добавлена!")
    
@router.callback_query(F.data == 'add')
async def add_note_callback(call: CallbackQuery, state: FSMContext):
    """Добавление заметки через inline кнопку"""
    await call.message.answer(" Введите текст заметки:")
    await state.set_state(index.add)
    await call.answer()
    
@router.message(index.add)
async def add_note_state(message: Message, state: FSMContext):
    """Получение текста заметки из FSM"""
    text = message.text.strip()
    if not text:
        await message.answer("⚠️ Текст не может быть пустым. Введите заметку:")
        return

    add_note(message.from_user.id, text)
    await message.answer("✅ Заметка добавлена!")
    await state.clear()
    
async def send_notes_list(user_id: int, send_func):
    '''функция вывода списка заметок'''
    notes = get_notes(user_id)
    if not notes:
        await send_func("У вас еще нет заметок.")
        return

    text = "📋 <b>Ваши заметки:</b>\n\n"

    for note in notes:
        date_str = note["da_te"].strftime("%Y-%m-%d %H:%M")
        note_text = note["text"]

        if len(note_text) > 30:
            chunks = [note_text[i:i+30] for i in range(0, len(note_text), 30)]
            note_text = "\n   ".join(chunks)

        if note["is_done"]:
            text += f"<s>{note['note_id']}. {note_text}</s>\n🕒 {date_str} ✅\n\n"
        else:
            text += f"{note['note_id']}. {note_text}\n🕒 {date_str}\n\n"

    await send_func(text)
    
@router.message(Command("list"))
async def list_notes_cmd(message: Message):
    await send_notes_list(
        user_id=message.from_user.id,
        send_func=lambda text: message.answer(text, parse_mode="HTML")
    )

@router.callback_query(F.data == "list")
async def list_notes_callback(call: CallbackQuery):
    await send_notes_list(
        user_id=call.from_user.id,
        send_func=lambda text: call.message.answer(text, parse_mode="HTML")
    )
    await call.answer()




'''Функция удаления заметки'''  
@router.message(Command("delete"))
async def delete_command(message: Message, state: FSMContext):
    args = message.text.replace("/delete", "").strip()
    
    if args and args.isdigit():
        note_id = int(args)
        delete_notes(message.from_user.id, note_id)
        await message.answer(f'Заметка {note_id} была удалена')
    else:
        # Если ID не передан, запрашиваем его
        await state.set_state(index.m_id)
        await message.answer("Введите номер заметки для удаления")



@router.callback_query(F.data == "delete")
async def get_id( call: CallbackQuery, state: FSMContext):
    await  call.message.answer("Введите номер заметки для удаления")
    await state.set_state(index.m_id)
    
@router.message(index.m_id)
async def del_note(message: Message,state: FSMContext):

    args = message.text.replace("/delete", "").strip()
    if not args.isdigit():
        await message.answer("Укажи ID заметки")
        return
    
    note_id = int(args)
    delete_notes(message.from_user.id, note_id)
    await message.answer(f'Заметка {note_id} была удалена')
    await state.clear()
    
'''зачеркивание заметки'''
@router.message(Command("cross"))
async def cross_cmd(message: Message, state: FSMContext):
    """Обработка команды /cross"""
    args = message.text.replace("/cross", "").strip()

    if args and args.isdigit():
        note_id = int(args)
        await handle_cross_action(message, message.from_user.id, note_id)
    else:
        # если ID не передан, просим пользователя ввести его
        await state.set_state(index.done)
        await message.answer("Введите ID заметки, которую хотите зачеркнуть:")


@router.callback_query(F.data == "cross")
async def cross_callback(call: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки 'перечеркнуть'"""
    await call.message.answer("Введите ID заметки, которую хотите зачеркнуть:")
    await state.set_state(index.done)
    await call.answer()


@router.message(index.done)
async def cross_state(message: Message, state: FSMContext):
    """FSM: пользователь вводит ID"""
    if not message.text.isdigit():
        await message.answer("⚠️ Введите корректный ID (число).")
        return

    note_id = int(message.text)
    await handle_cross_action(message, message.from_user.id, note_id)
    await state.clear()


async def handle_cross_action(message: Message, user_id: int, note_id: int):
    """Вспомогательная функция: зачёркивает / снимает зачёркивание"""
    crossed_note = done_task(user_id, note_id)

    if not crossed_note:
        await message.answer("❌ Такой заметки не существует.")
        return

    text = crossed_note["text"]
    is_done = crossed_note["is_done"]

    if is_done:
        await message.answer(f"✅ Заметка <b>«{text}»</b> зачёркнута.", parse_mode="HTML")
    else:
        await message.answer(f"Снято зачёркивание с <b>«{text}»</b>.", parse_mode="HTML")
