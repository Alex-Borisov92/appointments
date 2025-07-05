# app/main.py
from fastapi import FastAPI

from app.db import Base, engine
from app.routers import appointments

# ---------------------------------------------------------------------------#
# Создаём таблицы при старте приложения
# ---------------------------------------------------------------------------#
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointments Service")

# Подключаем роуты
app.include_router(appointments.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Простой health-check, который использует Docker HEALTHCHECK."""
    return {"status": "OK"}
