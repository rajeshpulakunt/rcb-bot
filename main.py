import requests
import time
import os
from bs4 import BeautifulSoup

# 🔗 URLs to monitor (add more if needed)
URLS = [
    "https://shop.royalchallengers.com/tickets"
]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 5  # seconds

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })
    except Exception as e:
        print("Telegram Error:", e)

def check_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text().lower()

        # 🎯 Smart detection
        if "buy tickets" in text or "book now" in text:
            return True

        if "tickets not available" in text or "sold out" in text:
            return False

        # fallback logic
        if "ticket" in text and "available" in text:
            return True

        return False

    except Exception as e:
        print("Check Error:", e)
        return False


print("🚀 Advanced RCB Bot Running...")

alert_active = False

while True:
    found = False

    for url in URLS:
        if check_page(url):
            found = True
            break

    if found:
        print("🔥 Tickets detected!")

        # 🔁 Send repeated alerts (3 times)
        for i in range(3):
            send_telegram(f"🔥 RCB TICKETS LIVE!\nGo FAST:\nhttps://shop.royalchallengers.com/")
            print(f"🚨 Alert {i+1} sent")
            time.sleep(2)

        alert_active = True

        # ⏸ Pause briefly to avoid spam
        time.sleep(60)

    else:
        if alert_active:
            print("🔄 Tickets gone / reset")
            alert_active = False

    time.sleep(CHECK_INTERVAL)
