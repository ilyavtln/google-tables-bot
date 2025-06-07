from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from admin.utils import user_is_admin
from utils.google_tables import (
    finish_last_task, get_all_tasks, get_active_tasks, get_stats, get_tasks_by_userid, get_unique_users
)
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
async def show_help(message: types.Message):
    await message.answer("Справка в разработке")


@router.message(Command("tasks"))
async def show_users_task(message: types.Message, worksheet):
    if user_is_admin(message.from_user.id):
        unique_users = await get_unique_users(worksheet)

        if not unique_users:
            await message.answer("В таблице пока нет пользователей.")
            return

        # Создаем инлайн-клавиатуру с callback_data в формате "user_123"
        builder = InlineKeyboardBuilder()
        for user_id, username in unique_users.items():
            builder.add(InlineKeyboardButton(
                text=username,
                callback_data=f"user_{user_id}"
            ))

        # Разбиваем кнопки по 2 в ряд
        builder.adjust(2)

        await message.answer(
            "Выберите пользователя для просмотра задач:",
            reply_markup=builder.as_markup()
        )
    else:
        tasks_messages = await get_tasks_by_userid(worksheet, message.from_user.id)

        if isinstance(tasks_messages, list):
            for msg in tasks_messages[1:]:
                await message.answer(msg)
        else:  # Если одно сообщение
            await message.answer(tasks_messages)


@router.message(Command("admin"))
async def admin_access(message: types.Message):
    if user_is_admin(message.from_user.id):
        await message.answer("Вы админ")


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

