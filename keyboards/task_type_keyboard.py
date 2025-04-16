from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_task_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Клинические исследования", callback_data="type_Клинические исследования"),
            InlineKeyboardButton(text="Разработка/Регистрация", callback_data="type_Разработка/Регистрация")
        ],
        [
            InlineKeyboardButton(text="БАД (перерегистрация, ДСС)", callback_data="type_БАД (перерегистрация, ДСС)"),
            InlineKeyboardButton(text="Отправка образцов на ФЭ", callback_data="type_Отправка образцов на ФЭ")
        ],
        [
            InlineKeyboardButton(text="Ответы на запросы", callback_data="type_Ответы на запросы"),
            InlineKeyboardButton(text="Внедрение", callback_data="type_Внедрение")
        ],
        [
            InlineKeyboardButton(text="Внесение изменений", callback_data="type_Внесение изменений"),
            InlineKeyboardButton(text="Проведение ТО АФС и ВВ", callback_data="type_Проведение ТО АФС и ВВ")
        ]
    ])
