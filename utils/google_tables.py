from core.base_utils import get_google_api_client, get_table_info
from utils.get_time import get_time


async def get_worksheet():
    google_client = get_google_api_client()

    table_name, list_name = get_table_info()

    agc = await google_client.authorize()
    sh = await agc.open(table_name)

    try:
        worksheet = await sh.worksheet(list_name)
    except:
        worksheet = await sh.add_worksheet(list_name, rows="1000", cols="6")
        await worksheet.append_row(["User ID", "Username", "Task", "Start Time", "End Time", "Type"])

    return worksheet


async def add_task(ws, user_id, username, task_name, task_type):
    now = get_time()
    await ws.append_row([str(user_id), username, task_name, now, "", task_type])


async def update_task_after_click():
    pass


async def finish_last_task(ws, user_id):
    rows = await ws.get_all_values()

    now = get_time()

    for i in range(len(rows) - 1, 0, -1):
        if len(rows[i]) >= 5 and rows[i][0] == str(user_id) and rows[i][4] == "":
            await ws.update_cell(i + 1, 5, now)
            return True
    return False


async def update_task_type_in_sheet(ws, user_id, task_type):
    rows = await ws.get_all_values()

    for i in range(len(rows) - 1, 0, -1):
        if rows[i][0] == str(user_id) and rows[i][5] == "":
            await ws.update_cell(i + 1, 6, task_type)
            break


async def get_all_tasks(ws):
    rows = await ws.get_all_values()
    return rows[1:]


async def get_active_tasks(ws):
    rows = await ws.get_all_values()
    return [row[1:4] + row[5:] for row in rows[1:] if len(row) > 4 and row[4] == ""]


async def get_stats(ws):
    """Возвращает форматированную строку со статистикой по задачам"""
    rows = await ws.get_all_values()

    if len(rows) < 2:
        return ""

    unique_users = set()
    completed = 0
    active = 0

    for row in rows[1:]:
        if len(row) < 6:
            continue

        user_id = row[0]
        username = row[1]
        end_time = row[4]

        unique_users.add(f"{username} (ID: {user_id})")

        if end_time.strip():
            completed += 1
        else:
            active += 1

    total = completed + active

    return (
        "<b>📊 Статистика задач:</b>\n"
        f"👥 Уникальные пользователи: {len(unique_users)}\n"
        f"✅ Выполнено задач: {completed}\n"
        f"🔄 Активных задач: {active}\n"
        f"📝 Всего задач: {total}"
    )


async def get_tasks_by_userid(ws, user_id):
    rows = await ws.get_all_values()
    user_tasks = []

    for row in rows[1:]:  # пропускаем заголовок
        if row and row[0] == str(user_id):  # проверяем ID пользователя
            user_tasks.append(row)

    if not user_tasks:
        return "У вас пока нет задач."

    formatted_tasks = []
    for i, task in enumerate(user_tasks, 1):
        status = "🔴 Активна" if len(task) < 5 or task[4] == "" else "✅ Завершена"
        task_type = task[5] if task[5] else "не указан"
        end_time = task[4] if len(task) > 4 and task[4] else "ещё не завершена"

        formatted_task = (
            f"{i}. <b>{task[2]}</b>\n"
            f"   🕒 Начата: {task[3]}\n"
            f"   🕓 Завершена: {end_time}\n"
            f"   🏷 Тип: {task_type}\n"
            f"   📌 Статус: {status}"
        )
        formatted_tasks.append(formatted_task)

    username = await get_username_by_id(ws, user_id) or f"User #{user_id}"
    header = f"📋 <b>Задачи пользователя @{username} ({len(user_tasks)}):</b>\n\n"

    return header + "\n\n".join(formatted_tasks)


async def get_unique_users(worksheet):
    rows = await worksheet.get_all_values()
    unique_users = {}

    for row in rows[1:]:  # Пропускаем заголовок
        if not row or len(row) < 2:  # Пропускаем пустые/неполные строки
            continue

        user_id = row[0].strip()  # ID пользователя (первая колонка)
        username = (row[1].strip() if len(row) > 1 and row[1].strip() else f"User #{user_id}")

        if user_id and user_id not in unique_users:
            unique_users[user_id] = username

    return unique_users


async def get_username_by_id(ws, user_id: str):
    rows = await ws.get_all_values()

    for row in rows[1:]:  # пропускаем заголовок
        if row and row[0] == str(user_id):  # проверяем ID пользователя
            return row[1] if len(row) > 1 and row[1] else ""  # возвращаем username (вторая колонка)

    return ""  # если пользователь не найден

