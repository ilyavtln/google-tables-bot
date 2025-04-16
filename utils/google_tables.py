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


# === 🔴 Завершить последнюю задачу ===
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