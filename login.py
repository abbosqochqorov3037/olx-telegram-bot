from telethon import TelegramClient
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

with TelegramClient("user_session", api_id, api_hash) as client:
    print("Telegram akkaunt ulandi!")
