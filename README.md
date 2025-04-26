# TWD Watcher

本專案會定時監控 MAX USDT/TWD 及即匯站 USD/TWD 匯率，當脫鉤超過 0.5% 時自動發送 Telegram 警示。

## 執行需求
- Python 3.13.2+
- 需設定以下環境變數：
  - `TELEGRAM_TOKEN`：你的 Telegram Bot Token
  - `TELEGRAM_CHAT_ID`：要發送訊息的 chat id

## Docker 執行方式

### 建立映像檔
```sh
docker build -t twd-watcher .
```

### 執行容器
```sh
docker run -d \
  -e TELEGRAM_TOKEN=你的token \
  -e TELEGRAM_CHAT_ID=你的chatid \
  --name twd-watcher \
  -p 8080:8080 \
  twd-watcher
```

- 服務會在 8080 port 提供 /health 健康檢查

## 主要檔案說明
- `twdWatcher.py`：主程式，負責匯率監控與警示

## 依賴套件
- aiohttp
- python-telegram-bot

## License
MIT
