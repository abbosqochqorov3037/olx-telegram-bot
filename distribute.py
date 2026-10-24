
import json
import os
from pathlib import Path

FILE = Path("elonlar.json")


def load_data():
    if not FILE.exists():
        print("elonlar.json topilmadi")
        return []

    data = json.loads(FILE.read_text(encoding="utf-8"))
    return data.get("elonlar", [])


def main():
    elonlar = load_data()

    if not elonlar:
        print("Tarqatish uchun e'lon yo'q.")
        return

    # Kanal identifikatorlari CHANNELS secretida vergul bilan ajratiladi.
    channels = [
        x.strip()
        for x in os.environ.get("CHANNELS", "").split(",")
        if x.strip()
    ]

    if not channels:
        print("CHANNELS sozlanmagan. Hozircha hech narsa yuborilmadi.")
        return

    print(f"{len(elonlar)} ta e'lon va {len(channels)} ta kanal topildi.")
    print("Telegram ulanishi va kanal ruxsatlari sozlanmagani uchun yuborish bajarilmadi.")


if __name__ == "__main__":
    main()
