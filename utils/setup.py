from aiogram import Bot
from aiogram.types import BotCommand


async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Запустить бота'),
        BotCommand(command='/new', description='Начать задачу'),
        BotCommand(command='/end', description='Завершить задачу'),
        BotCommand(command='/help', description='Помощь')
    ]
    await bot.set_my_commands(commands)