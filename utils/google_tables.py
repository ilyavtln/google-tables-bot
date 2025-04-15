from datetime import datetime

from core.base_utils import get_google_api_client, get_table_info


async def get_worksheet():
    google_client = get_google_api_client()

    table_name, list_name = get_table_info()

    agc = await google_client.authorize()
    sh = await agc.open(table_name)

    try:
        worksheet = await sh.worksheet(list_name)
    except:
        worksheet = await sh.add_worksheet(list_name, rows="1000", cols="5")
        await worksheet.append_row(["User ID", "Username", "Task", "Start Time", "End Time"])

    return worksheet


async def add_task(ws, user_id, username, task_name):
    now = datetime.now().strftime("%d%m-%Y %H:%M:%S")
    await ws.append_row([str(user_id), username, task_name, now, ""])


# === 🔴 Завершить последнюю задачу ===
async def finish_last_task(ws, user_id):
    rows = await ws.get_all_values()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i in range(len(rows) - 1, 0, -1):
        if len(rows[i]) >= 5 and rows[i][0] == str(user_id) and rows[i][4] == "":
            await ws.update_cell(i + 1, 5, now)
            return True
    return False


async def get_all_tasks(ws):
    rows = await ws.get_all_values()
    return rows[1:]