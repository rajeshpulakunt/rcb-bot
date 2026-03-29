import requests
import time
import os
from bs4 import BeautifulSoup

# 🔗 Target URL
URL = "https://shop.royalchallengers.com/tickets"

# 🔐 Environment variables (Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ⏱ Check interval (seconds)
CHECK_INTERVAL = 5

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })
        print("📩 Alert sent:", response.status_code)
    except Exception as e:
        print("Telegram Error:", e)

def check_ticket():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text().lower()

        # 🔍 Condition
        if "tickets not available" not in text:
            return True
        return False

    except Exception as e:
        print("Check Error:", e)
        return False


print("🚀 RCB Ticket Bot Started...")

alert_sent = False

while True:
    available = check_ticket()

    if available and not alert_sent:
        send_telegram("🔥 RCB TICKETS ARE LIVE!\nhttps://shop.royalchallengers.com/")
        print("🚨 ALERT SENT")
        alert_sent = True

    elif not available:
        alert_sent = False

    time.sleep(CHECK_INTERVAL)
