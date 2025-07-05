<!-- docs/architecture.md -->

# Архитектурная схема «Appointments Service»

```mermaid
flowchart TD
    subgraph FastAPI App [FastAPI приложение]
        direction TB
        A1[main.py<br/>— точка входа<br/>— FastAPI() + роуты] --> A2
        A2[routers/appointments.py<br/>— POST/GET эндпойнты] --> A3
        A3[schemas.py<br/>— Pydantic<br/>Request / Response] --> A4
        A2 --> A4
        A4[models.py<br/>— SQLAlchemy ORM<br/>Appointment] --> A5
        A5[db.py<br/>— engine / SessionLocal<br/>Base.metadata.create_all]
    end

    FastAPI App -->|SQLAlchemy Session| PG[(PostgreSQL DB<br/>appointments table)]
    PG -->|Unique index<br/>doctor_id+start_time| PG

    style PG fill:#f3f9ff,stroke:#3b82f6,stroke-width:2px
    style FastAPI App fill:#fff9f0,stroke:#f97316,stroke-width:2px
