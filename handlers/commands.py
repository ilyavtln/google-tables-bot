from aiogram import Router, types
from aiogram.filters import Command
from aiogram import Bot
from core.base_utils import get_admins_ids
from utils.google_tables import finish_last_task, add_task

router = Router()
admins = get_admins_ids()

@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    user_id = message.from_user.id

    if user_id in admins:
        await message.answer("Привет админ")
        return

    await message.answer("Привет! Я бот для работы с гугл таблицами.")


@router.message(Command("new"))
async def start_new_task(message: types.Message, worksheet):
    # Завершаем последнюю задачу перед началом новой
    await finish_last_task(worksheet, message.from_user.id)

    # Добавляем новую задачу
    await add_task(
        worksheet,
        user_id=message.from_user.id,
        username=message.from_user.username or message.from_user.full_name,
        task_name=message.text.strip()
    )


@router.message(Command("end"))
async def end_last_task(message: types.Message, worksheet):
    # Завершаем последнюю задачу перед началом новой
    await finish_last_task(worksheet, message.from_user.id)

    await message.answer("Последняя задача отмечена как завершенная")


@router.message(Command("help"))
async def end_last_task(message: types.Message):
    await message.answer("Справка в разработке")


@router.message(Command("admin"))
async def admin_access(message: types.Message):
    user_id = message.from_user.id

    if user_id in admins:
        await message.answer("Вы админ")
        return
    else:
        await message.answer(f"Ваш id {user_id}, вы не админ")


