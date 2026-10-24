import os
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
    "@Toshkent_kvartira_ijara_24",
    "@Toshkent_talabalarga_kvartira",
    "@Studentlarga_kvartira_arenda_ij",
    "@Studentlarga_kvartira_arenda_ija",
    "@Kvartira_bezmakler_studentlarga",
    "@Toshkent_uy_oldi_sotdi_bozori",
    "@Toshkent_kvartira_bezmakler_ijar",
    "@Kvartira_toshkent_maklersiz_aren",
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
