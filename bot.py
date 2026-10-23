import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://www.olx.uz/nedvizhimost/kvartiry/arenda-kvartir/tashkent/"

def main():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("div[data-cy='l-card']")

    for card in cards:
        link = card.select_one("a[href]")
        title = card.select_one("h6, h4")

        if not link or not title:
            continue

        ad_url = urljoin("https://www.olx.uz", link["href"])
        ad_title = title.get_text(" ", strip=True)

        message = f"🏠 {ad_title}\n🔗 {ad_url}"

        result = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message},
            timeout=30
        )
        result.raise_for_status()

if __name__ == "__main__":
    main()
