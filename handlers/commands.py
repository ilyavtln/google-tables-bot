from aiogram import Router, types, Bot
from aiogram.filters import Command
from admin.utils import user_is_admin
from utils.google_tables import finish_last_task, get_all_tasks, get_active_tasks, get_stats
from utils.setup import setup_bot_commands

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    await setup_bot_commands(bot, message.from_user.id)

    if user_is_admin(message.from_user.id):
        await message.answer(f"Привет админ")
        return

    await message.answer("Привет! Я бот для работы с гугл таблицами.")


@router.message(Command("new"))
async def start_new_task(message: types.Message):
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
    if user_is_admin(message.from_user.id):
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


@router.message(Command("active"))
async def active_tasks(message: types.Message, worksheet):
    if user_is_admin(message.from_user.id):
        # Получение всех задач
        rows = await get_active_tasks(worksheet)

        if not rows:
            await message.answer("Задач пока нет.")
            return

        # Формируем список задач
        task_list = "\n\n".join(
            [f"Задача #{i + 1}:\n" + "\n".join(f"{col}" for col in row) for i, row in enumerate(rows)]
        )

        await message.answer(task_list)


@router.message(Command("stats"))
async def active_tasks(message: types.Message, worksheet):
    if user_is_admin(message.from_user.id):
        stats = await get_stats(worksheet)

        await message.answer(stats)

