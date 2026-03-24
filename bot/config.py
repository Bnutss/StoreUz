import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
WEBAPP_URL: str = os.getenv('WEBAPP_URL', '')
ADMIN_IDS: list[int] = [
    int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip().isdigit()
]
