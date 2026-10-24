fimport os
import json
import requests
from pathlib import Path

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
FILE = Path("elonlar.json")

def main():
    if not TOKEN:
        print("XATO: bot tokeni sozlanmagan")
        return

    if not FILE.exists():
        print("elonlar.json topilmadi")
        return

    data = json.loads(FILE.read_text(encoding="utf-8"))
    elonlar = data.get("elonlar", [])

    channels = [
        x.strip()
        for x in os.environ.get("CHANNELS", "").split(",")
        if x.strip()
    ]

    if not elonlar:
        print("Saqlangan e'lon yo'q")
        return

    if not channels:
        print("Kanallar ro'yxati sozlanmagan")
        return

    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for kanal in channels:
        for elon in elonlar:
            try:
                r = requests.post(
                    api,
                    json={
                        "chat_id": kanal,
                        "text": elon
                    },
                    timeout=30
                )
                result = r.json()

                if result.get("ok"):
                    print(f"Yuborildi: {kanal}")
                else:
                    print(f"Yuborilmadi: {kanal}: "
                          f"{result.get('description')}")

            except Exception as e:
                print(f"Xato: {kanal}: {e}")

if __name__ == "__main__":
    main()
