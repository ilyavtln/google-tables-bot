import os
import gspread_asyncio
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


def get_bot_token():
    """
    Получает токен бота из переменных окружения.
    """
    load_dotenv()

    return os.getenv("BOT_TOKEN")


def get_admins_ids():
    """
    Получает id админов из переменных окружения.
    """
    load_dotenv()

    admin_ids = os.getenv("ADMINS").split(",")
    return list(map(int, admin_ids))


def get_google_api_client():
    """Возвращает асинхронного клиента для Google Sheets API."""

    def get_creds():
        return ServiceAccountCredentials.from_json_keyfile_name(
            'core/creds.json',
            ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )

    return gspread_asyncio.AsyncioGspreadClientManager(get_creds)


def get_table_info():
    """
    Возвращает название таблицы и активного листа
    """
    load_dotenv()

    table_name = os.getenv("TABLE_NAME")
    list_name = os.getenv("LIST_NAME")

    return table_name, list_name
