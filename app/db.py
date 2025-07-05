# app/db.py
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# ---------------------------------------------------------------------------#
# Строка подключения:
# - если переменная окружения DATABASE_URL не задана, используем SQLite
#   в оперативной памяти (удобно для pytest).
# ---------------------------------------------------------------------------#
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# ---------------------------------------------------------------------------#
# Создаём движок SQLAlchemy.
# Для in-memory SQLite нужен StaticPool, чтобы все сессии разделяли
# один и тот же connection (и не теряли таблицы между запросами).
# ---------------------------------------------------------------------------#
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
        future=True,
    )
else:
    engine = create_engine(DATABASE_URL, echo=False, future=True)

# ---------------------------------------------------------------------------#
# Фабрика сессий и базовый класс моделей
# ---------------------------------------------------------------------------#
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)
Base = declarative_base()


# ---------------------------------------------------------------------------#
# Dependency для FastAPI — даёт и закрывает сессию.
# (Полезно, если хотите убрать копипасту из роутеров.)
# ---------------------------------------------------------------------------#
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
