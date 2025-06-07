from aiogram import Router, types, F
from utils.google_tables import update_task_type_in_sheet, get_tasks_by_userid

router = Router()


@router.callback_query(F.data.startswith("type_"))
async def handle_task_type_callback(callback: types.CallbackQuery, worksheet):
    task_type = callback.data.replace("type_", "")

    await update_task_type_in_sheet(
        worksheet,
        user_id=callback.from_user.id,
        task_type=task_type
    )

    await callback.answer(f"Тип задачи обновлён: {task_type}")
    await callback.message.edit_text(f"Тип задачи обновлён: {task_type} ✅")


@router.callback_query(F.data.startswith("user_"))
async def handle_user_selection(callback: types.CallbackQuery, worksheet):
    # Извлекаем user_id из callback_data
    user_id = callback.data.replace("user_", "")

    # Получаем задачи выбранного пользователя
    tasks = await get_tasks_by_userid(worksheet, user_id)

    await callback.message.edit_text(
        text=tasks,
        reply_markup=None  # Убираем клавиатуру после выбора
    )