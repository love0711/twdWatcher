# 使用更小的 Python 3.13.2-alpine 映像
FROM python:3.13.2-alpine

# 設定工作目錄
WORKDIR /app

# 安裝必要的系統套件（安裝完即移除 build-base）
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev && \
    pip install --no-cache-dir aiohttp python-telegram-bot && \
    apk del .build-deps

# 複製程式碼
COPY twdWatcher.py ./

# 設定環境變數（可於 docker run 時覆蓋）
ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# 啟動指令
CMD ["python", "twdWatcher.py"]
