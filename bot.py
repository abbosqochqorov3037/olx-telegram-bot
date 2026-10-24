import os
import json
import requests
from pathlib import Path

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}/"
FILE = Path("elonlar.json")


def load_data():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    return {"elonlar": []}


def save_data(data):
    FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def send_message(chat_id, text):
    response = requests.post(
        API + "sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def main():
    offset = None
    print("Bot ishga tushdi!")

    while True:
        try:
            result = requests.get(
                API + "getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35
            ).json()

            if not result.get("ok"):
                print("Telegram API xatosi:", result)
                continue

            for update in result.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "").strip()

                if not chat_id or not text:
                    continue

                if text == "/start":
                    send_message(
                        chat_id,
                        "Salom! 🏠\n\n"
                        "Kvartira e'lonini matn ko'rinishida yuboring.\n"
                        "/royxat — saqlangan e'lonlar soni."
                    )

                elif text == "/royxat":
                    data = load_data()
                    send_message(
                        chat_id,
                        f"Saqlangan e'lonlar soni: {len(data['elonlar'])}"
                    )

                else:
                    data = load_data()
                    data["elonlar"].append(text)
                    save_data(data)
                    send_message(
                        chat_id,
                        f"✅ E'lon saqlandi!\n"
                        f"Jami: {len(data['elonlar'])} ta."
                    )

        except Exception as error:
            print("Xato:", error)


if __name__ == "__main__":
    main()
