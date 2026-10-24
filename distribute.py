import os
import json
import asyncio
from pathlib import Path
from telethon import TelegramClient
from telethon.sessions import StringSession

# GitHub Secrets orqali olinadi
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["TELEGRAM_SESSION"]

# E'lonlar fayli
FILE = Path("elonlar.json")

# Telegram kanallari
CHANNELS = [
    "@Toshkent_kvartira_ijara_24",
    "@Toshkent_talabalarga_kvartira",
    "@Studentlarga_kvartira_arenda_ij",
    "@Studentlarga_kvartira_arenda_ija",
    "@toshkent_bezmakler_kvartira",
    "@Toshkent_uy_oldi_sotdi_bozori",
    "@Toshkent_kvartira_bezmakler_ijar",
    "@Kvartira_toshkent_maklersiz_aren",
]


async def main():
    if not FILE.exists():
        print("XATO: elonlar.json fayli topilmadi.")
        return

    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"E'lonlar faylini o'qishda xato: {e}")
        return

    elonlar = data.get("elonlar", [])

    if not elonlar:
        print("Saqlangan e'lon yo'q.")
        return

    async with TelegramClient(
        StringSession(SESSION),
        API_ID,
        API_HASH
    ) as client:

        for channel in CHANNELS:
            for elon in elonlar:
                try:
                    await client.send_message(channel, elon)
                    print(f"Yuborildi: {channel}")
                    await asyncio.sleep(3)

                except Exception as e:
                    print(f"XATO — {channel}: {e}")

    print("Tarqatish yakunlandi.")


if __name__ == "__main__":
    asyncio.run(main())
