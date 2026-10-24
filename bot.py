import os
import json
import time
import base64
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GH_TOKEN = os.environ["GH_TOKEN"]
REPO = "abbosqochqorov3037/olx-telegram-bot"
FILE = "elonlar.json"

TG_API = f"https://api.telegram.org/bot{TOKEN}/"
GH_API = f"https://api.github.com/repos/{REPO}/contents/{FILE}"


def github_read():
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(GH_API, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()
    content = base64.b64decode(result["content"]).decode("utf-8")
    return json.loads(content), result["sha"]


def github_save(data, sha):
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    content = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": "Telegram e'lonlarini saqlash",
        "content": content,
        "sha": sha
    }

    response = requests.put(
        GH_API,
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()


def send_message(chat_id, text):
    response = requests.post(
        TG_API + "sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30
    )
    response.raise_for_status()


def main():
    offset = None
    print("Bot ishga tushdi!")

    while True:
        try:
            response = requests.get(
                TG_API + "getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35
            )
            response.raise_for_status()
            result = response.json()

            if not result.get("ok"):
                time.sleep(3)
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
                        "🏠 E'lon saqlash botiga xush kelibsiz!\n\n"
                        "E'lon matnini yuboring.\n"
                        "/royxat — e'lonlar soni."
                    )

                elif text == "/royxat":
                    data, _ = github_read()
                    send_message(
                        chat_id,
                        f"Saqlangan e'lonlar: {len(data['elonlar'])} ta"
                    )

                else:
                    data, sha = github_read()
                    data.setdefault("elonlar", []).append(text)
                    github_save(data, sha)

                    send_message(
                        chat_id,
                        f"✅ E'lon GitHub'ga saqlandi!\n"
                        f"Jami: {len(data['elonlar'])} ta."
                    )

        except Exception as error:
            print("Xato:", error)
            time.sleep(3)


if __name__ == "__main__":
    main()
