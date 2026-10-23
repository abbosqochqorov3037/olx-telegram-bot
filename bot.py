import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def main():
    text = (
        "🤖 OLX Telegram bot ishga tushdi!\n\n"
        "Bu sinov xabari. Telegramga yuborish ishlayaptimi, tekshiramiz."
    )

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=30
    )
    print("Telegram javobi:", response.text)
response.raise_for_status()
print("Telegramga xabar yuborildi!")

if __name__ == "__main__":
    main()
