from fastapi import FastAPI
from app.db import engine
from app import models
from app.routes import auth, info, send_coin, buy

app = FastAPI(title="Avito Shop API", version="1.0.0")

# Создаем все таблицы (на старте приложения)
models.Base.metadata.create_all(bind=engine)

# Подключаем маршруты (каждый маршрут будет иметь префикс /api)
app.include_router(auth.router, prefix="/api")
app.include_router(info.router, prefix="/api")
app.include_router(send_coin.router, prefix="/api")
app.include_router(buy.router, prefix="/api")
