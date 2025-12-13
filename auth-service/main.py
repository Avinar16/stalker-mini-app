import os
import hmac
import hashlib
from urllib.parse import parse_qsl
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Разрешаем все origins (только для теста!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Укажите ваш токен бота здесь (или через переменную окружения)
BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.post("/auth/verify")
def verify_telegram_auth(payload: dict):
    init_data = payload.get("initData", "")

    if not init_data:
        raise HTTPException(status_code=400, detail="initData is required")

    # Парсим параметры
    try:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        hash_ = parsed.pop("hash", None)
        if not hash_:
            raise HTTPException(status_code=400, detail="Missing hash")

        # Проверка подписи
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(computed_hash, hash_):
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Извлекаем данные пользователя
        user_data = eval(parsed["user"])  # Telegram передаёт user как строку-словарь
        user_id = int(user_data["id"])
        first_name = user_data.get("first_name", "")

        # ✅ Аутентификация успешна!
        return {
            "status": "ok",
            "user_id": user_id,
            "first_name": first_name
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")