# Appointments Service

Микросервис записи пациентов на приём. Реализован на FastAPI, использует PostgreSQL в проде и SQLite in-memory в тестах. Врачу гарантируется уникальность пары `doctor_id + start_time`.

---

## Быстрый запуск < 1 мин

```bash
# 1. клонируем
git clone https://github.com/your-org/appointments.git
cd appointments

# 2. настраиваем переменные окружения
cp .env.example .env

# 3. собираем и поднимаем контейнеры
docker compose up -d --build

# 4. проверяем, что сервис жив
curl http://localhost:8000/health        # → {"status":"OK"}

# 5. создаём тестовую запись
curl -X POST http://localhost:8000/appointments \
     -H "Content-Type: application/json" \
     -d '{"doctor_id": 1, "patient_name": "Demo", "start_time": "2030-01-01T09:00:00"}'

Swagger-UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```
---

## Полезные команды Make

| цель          | действие                               |
| ------------- | -------------------------------------- |
| `make up`     | docker compose up -d --build           |
| `make down`   | docker compose down                    |
| `make lint`   | flake8 + isort --check + black --check |
| `make format` | автоформатирование isort + black       |
| `make test`   | pytest (юнит + интеграция)             |

---

## API кратко

| метод | путь                 | описание                    |
| ----- | -------------------- | --------------------------- |
| POST  | `/appointments`      | создать запись              |
| GET   | `/appointments/{id}` | получить запись по ID       |
| GET   | `/health`            | проверка живости контейнера |

---

## CI

GitHub Actions запускает две стадии:

1. **Lint** — `make lint`
2. **Tests** — `make test`
   Service-container Postgres поднимается для интеграционных тестов.

При пуше в ветку `main` дополнительно собирается и пушится Docker-образ в GHCR.

---

## Схемы и документы

* `docs/architecture.png` — схема модулей сервиса
* `docs/erd.png` — ER-диаграмма
* `docs/activity.png` — activity диаграмма сценария записи
* `docs/bp.md` — бизнес-процесс и роли
* `bot/` — набросок telegram-бота с AI-подбором врача

---

## answers.txt

```text
python: 9
fastapi: 8
docker: 8
github actions: 7
sql: 7
ai code: 6
biz integration: 8
english: 9
tasks: scrum
```

---

© 2025 Борисов Александр. Используйте и расширяйте по своему усмотрению.
