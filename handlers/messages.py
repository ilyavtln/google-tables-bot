from aiogram import Router
from aiogram import F
from aiogram.types import Message
from keyboards.task_type_keyboard import get_task_type_keyboard
from utils.google_tables import add_task, finish_last_task

router = Router()

# Обработчик точного текста "Привет"
@router.message(F.text == "Привет")
async def echo_hello(message: Message, worksheet):
    await message.answer(f"Привет! Работаем с таблицей: {worksheet.title}")


# Обработчик любого текста (кроме команд)
@router.message(F.text)
async def handle_task_start(message: Message, worksheet):
    # Завершить предыдущую задачу
    await finish_last_task(worksheet, message.from_user.id)

    # Добавить новую задачу с пустым типом
    await add_task(
        worksheet,
        user_id=message.from_user.id,
        username=message.from_user.username or message.from_user.full_name,
        task_name=message.text.strip(),
        task_type=""
    )

    # Клавиатура с выбором типа
    await message.answer("Задача начата! Выберите тип задачи (не обязательно):", reply_markup=get_task_type_keyboard())