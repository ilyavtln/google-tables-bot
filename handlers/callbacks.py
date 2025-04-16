from aiogram import Router, types, F
from utils.google_tables import update_task_type_in_sheet

router = Router()


@router.callback_query(F.data.startswith("type_"))
async def handle_task_type_callback(callback: types.CallbackQuery, worksheet):
    task_type = callback.data.replace("type_", "")

    await update_task_type_in_sheet(
        worksheet,
        user_id=callback.from_user.id,
        task_type=task_type
    )

    await callback.answer(f"Тип задачи обновлён: {task_type or 'пропущен'}")
    await callback.message.edit_text(f"Тип задачи обновлён: {task_type or 'пропущен'} ✅")