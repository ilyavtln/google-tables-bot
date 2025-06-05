from aiogram import Bot
from aiogram.types import BotCommand
from admin.utils import user_is_admin


async def setup_bot_commands(bot: Bot, user_id: int = None):
    is_admin = user_is_admin(user_id)

    # Базовые команды для всех пользователей
    user_commands = [
        BotCommand(command='/start', description='Запустить бота'),
        BotCommand(command='/new', description='Начать задачу'),
        BotCommand(command='/end', description='Завершить задачу'),
        BotCommand(command='/help', description='Помощь')
    ]

    # Команды только для админов
    admin_commands = [
        BotCommand(command="/admin", description="Админ панель"),
        BotCommand(command="/active", description="Активные задачи"),
        BotCommand(command="/stats", description="Статистика")
    ]

    # Объединяем команды, если пользователь админ
    commands = user_commands + admin_commands if is_admin else user_commands

    # Устанавливаем команды
    await bot.set_my_commands(commands=commands)