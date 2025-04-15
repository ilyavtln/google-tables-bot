from aiogram import Router, types
from aiogram.filters import Command
from aiogram import Bot
from core.base_utils import get_admins_ids
from utils.google_tables import finish_last_task, add_task, get_all_tasks

router = Router()
admins = get_admins_ids()

@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    user_id = message.from_user.id

    if user_id in admins:
        await message.answer(f"Привет админ")
        return

    await message.answer("Привет! Я бот для работы с гугл таблицами.")


@router.message(Command("new"))
async def start_new_task(message: types.Message, worksheet):
    await message.answer("Введите название задачи")


@router.message(Command("end"))
async def end_last_task(message: types.Message, worksheet):
    # Завершаем последнюю задачу перед началом новой
    await finish_last_task(worksheet, message.from_user.id)

    await message.answer("Последняя задача отмечена как завершенная")


@router.message(Command("help"))
async def end_last_task(message: types.Message):
    await message.answer("Справка в разработке")


@router.message(Command("admin"))
async def admin_access(message: types.Message, worksheet):
    user_id = message.from_user.id

    if user_id in admins:
        await message.answer("Вы админ")

        # Получение всех задач
        rows = await get_all_tasks(worksheet)

        if not rows:
            await message.answer("Задач пока нет.")
            return

        # Формируем список задач
        task_list = "\n\n".join(
            [f"Задача #{i + 1}:\n" + "\n".join(f"{col}" for col in row) for i, row in enumerate(rows)]
        )

        await message.answer(task_list)

    else:
        await message.answer(f"Ваш id {user_id}, вы не админ")



