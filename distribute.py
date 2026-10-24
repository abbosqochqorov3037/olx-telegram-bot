import os
import json
from pathlib import Path
from telethon import TelegramClient

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["TELEGRAM_SESSION"]

FILE = Path("elonlar.json")

CHANNELS = [
    "@Toshkent_kvartira_ijara_24",
    "@Toshkent_talabalarga_kvartira",
    "@Studentlarga_kvartira_arenda_ij",
    "@Studentlarga_kvartira_arenda_ija",
    "@Kvartira_bezmakler_studentlarga",
    "@Toshkent_uy_oldi_sotdi_bozori",
    "@Toshkent_kvartira_bezmakler_ijar",
    "@Kvartira_toshkent_maklersiz_aren",
]

async def main():
    if not FILE.exists():
        print("elonlar.json topilmadi")
        return

    data = json.loads(FILE.read_text(encoding="utf-8"))
    elonlar = data.get("elonlar", [])

    if not elonlar:
        print("Saqlangan e'lon yo'q")
        return

    async with TelegramClient(
        "user_session",
        API_ID,
        API_HASH
    ) as client:
        for channel in CHANNELS:
            for elon in elonlar:
                try:
                    await client.send_message(channel, elon)
                    print(f"Yuborildi: {channel}")
                except Exception as e:
                    print(f"Yuborilmadi: {channel}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
