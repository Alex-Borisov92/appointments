# Архитектурная схема «Appointments Service»

```mermaid
flowchart TD
    %% === Слой приложения (FastAPI) ===
    subgraph fastapi["FastAPI приложение"]
        direction TB
        A1([main.py<br/>- точка входа]) --> A2[routers/appointments.py<br/>POST + GET]
        A2 --> A3[schemas.py<br/>Request ↔ Response]
        A3 --> A4[models.py<br/>SQLAlchemy ORM <Appointment>]
        A4 --> A5[db.py<br/>engine / SessionLocal]
    end

    %% === Слой данных ===
    subgraph pg["PostgreSQL DB"]
        D[(appointments<br/>UNIQUE doctor_id + start_time)]
    end

    %% === Связи между слоями ===
    fastapi -->|SQLAlchemy Session| D

    %% === Стили ===
    classDef box fill:#f9f9ff,stroke:#4973b6,stroke-width:2px;
    classDef db fill:#f3f9ff,stroke:#3b82f6,stroke-width:2px;

    class fastapi box;
    class pg db;
````