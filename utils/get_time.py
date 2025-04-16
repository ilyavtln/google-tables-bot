from datetime import datetime
from zoneinfo import ZoneInfo

def get_time():
    return datetime.now(ZoneInfo("Asia/Novosibirsk")).strftime("%d.%m.%Y %H:%M:%S")

