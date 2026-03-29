import requests
import time
import os

URL = "https://shop.royalchallengers.com/tickets"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 3  # ⚡ faster

session = requests.Session()

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        session.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram Error:", e)

def fast_check():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
            "Connection": "keep-alive"
        }

        res = session.get(URL, headers=headers, timeout=5)
        text = res.text.lower()

        # ⚡ FAST KEY SIGNALS
        if "buy tickets" in text or "add to cart" in text:
            return True

        if "tickets not available" in text or "sold out" in text:
            return False

        # fallback signal
        if "ticket" in text and "₹" in text:
            return True

        return False

    except Exception as e:
        print("Check Error:", e)
        return False


print("🚀 ULTRA FAST BOT RUNNING...")

alert_active = False

while True:
    available = fast_check()

    if available:
        print("🔥 DETECTED!")

        # 🔁 Rapid burst alerts
        for i in range(5):
            send_telegram("🔥🔥 RCB TICKETS LIVE NOW!\nhttps://shop.royalchallengers.com/")
            time.sleep(1)

        alert_active = True

        # ⏸ cooldown
        time.sleep(45)

    else:
        if alert_active:
            print("🔄 Reset state")
            alert_active = False

    time.sleep(CHECK_INTERVAL)
