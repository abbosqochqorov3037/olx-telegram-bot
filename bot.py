import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def main():
    text = "🤖 OLX bot sinov xabari!"

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )

    print("Telegram javobi:", response.text)
    response.raise_for_status()
    print("Xabar yuborildi!")

if __name__ == "__main__":
    main()
