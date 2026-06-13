import requests
import yfinance as yf
import time
from datetime import datetime
from config import SELL_ZONE_LOW, SELL_ZONE_HIGH, SL_SELL, TP_SELL
from config import BUY_ZONE_LOW, BUY_ZONE_HIGH, SL_BUY, TP_BUY

TOKEN = "8711310335:AAEloHto_g4eA-2b7qSP0CpvsPtQfJeUmjA"
CHAT_ID = "8340091131"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_gold_price():
    gold = yf.Ticker("GC=F")
    price = gold.history(period="1d")["Close"].iloc[-1]
    return round(price, 2)

def save_log(signal, price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("log.txt", "a") as f:
        f.write(f"{now} | {signal} | 价格：{price}\n")

print("🤖 黄金机器人启动...")
send_telegram(f"🤖 黄金机器人启动！\n🔴 做空区域：{SELL_ZONE_LOW}-{SELL_ZONE_HIGH}\n🟢 做多区域：{BUY_ZONE_LOW}-{BUY_ZONE_HIGH}")

last_signal = None

while True:
    price = get_gold_price()
    print(f"当前价格：{price}")

    if SELL_ZONE_LOW <= price <= SELL_ZONE_HIGH:
        if last_signal != "SELL":
            send_telegram(f"🔴 进入做空区域！\n价格：{price}\nSL：{SL_SELL} TP：{TP_SELL}")
            save_log("SELL信号", price)
            last_signal = "SELL"

    elif BUY_ZONE_LOW <= price <= BUY_ZONE_HIGH:
        if last_signal != "BUY":
            send_telegram(f"🟢 进入做多区域！\n价格：{price}\nSL：{SL_BUY} TP：{TP_BUY}")
            save_log("BUY信号", price)
            last_signal = "BUY"

    else:
        if last_signal in ["SELL", "BUY"]:
            send_telegram(f"⚪ 离开信号区域。价格：{price}")
            save_log("离开区域", price)
        last_signal = "OTHER"

    time.sleep(300)
