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
        image = card.select_one("img")
        price = card.select_one("[data-testid='ad-price']")

        if not link or not title:
            continue

        ad_url = urljoin("https://www.olx.uz", link["href"])
        ad_title = title.get_text(" ", strip=True)
        ad_price = price.get_text(" ", strip=True) if price else "Narx ko‘rsatilmagan"
        photo = image.get("src") if image else None

        text = (
            f"🏠 {ad_title}\n"
            f"💰 {ad_price}\n"
            f"🔗 {ad_url}"
        )

        api = f"https://api.telegram.org/bot{TOKEN}/"

        if photo:
            result = requests.post(
                api + "sendPhoto",
                data={
                    "chat_id": CHAT_ID,
                    "photo": photo,
                    "caption": text[:1000]
                },
                timeout=30
            )
            if result.ok:
                continue

        requests.post(
            api + "sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=30
        ).raise_for_status()


if __name__ == "__main__":
    main()
