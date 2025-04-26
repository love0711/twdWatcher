import asyncio
import aiohttp
import time
import json
import os
from telegram import Bot
from aiohttp import web

# 設定
MAX_REST_URL = "https://max-api.maicoin.com/api/v3/wallet/m/index_prices"
# 使用即匯站 API 查詢 USD/TWD 匯率
JI_HUI_ZHAN_URL = "https://tw.rter.info/capi.php"

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
THRESHOLD = 0.005  # 0.5% 脫鉤門檻

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(text):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

async def fetch_max_price(session):
    async with session.get(MAX_REST_URL) as resp:
        data = await resp.json()
        # USDT/TWD 匯率在 'usdttwd' 欄位（全小寫）
        price = float(data["usdttwd"])
        return price

async def fetch_jihuizhan_price(session):
    async with session.get(JI_HUI_ZHAN_URL) as resp:
        text = await resp.text()
        data = json.loads(text)
        price = float(data["USDTWD"]["Exrate"])
        return price

async def monitor_arbitrage():
    last_alert_time = 0
    async with aiohttp.ClientSession() as session:
        while True:
            max_price = await fetch_max_price(session)
            jihuizhan_price = await fetch_jihuizhan_price(session)
            if max_price and jihuizhan_price:
                diff = (max_price - jihuizhan_price) / jihuizhan_price
                print(diff)
                now = time.time()
                if abs(diff) >= THRESHOLD:
                    if now - last_alert_time >= 300:
                        direction = "高於" if diff > 0 else "低於"
                        msg = f"脫鉤警示：MAX USDT/TWD 報價 {max_price}，即匯站 USD/TWD 報價 {jihuizhan_price}，MAX 報價{direction} 即匯站 {abs(diff)*100:.2f}%"
                        await send_telegram_message(msg)
                        last_alert_time = now
            await asyncio.sleep(5)  # 每5秒輪詢一次

async def health(request):
    return web.Response(text="OK")

async def start_health_server():
    app = web.Application()
    app.router.add_get('/health', health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

async def main():
    await asyncio.gather(
        monitor_arbitrage(),
        start_health_server()
    )

if __name__ == "__main__":
    asyncio.run(main())