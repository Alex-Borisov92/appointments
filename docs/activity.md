<!-- docs/activity.md -->

# Activity-диаграмма сценария «Пациент записывается на приём»

```mermaid
flowchart TD
    %% swim-lanes (псевдо) слева-направо
    subgraph L1["👤 Пациент"]
        P0([Запустить интерфейс<br/>или Telegram-бот])
        P1([Ввести жалобы<br/>или выбрать врача])
        P2([Выбрать свободное время])
        P3([Получить подтверждение])
    end

    subgraph L2["🤖 Интерфейс / Бот"]
        B0([Запросить симптомы])
        B1([Определить специальность<br/>(ML / LLM)])
        B2([Запросить слоты у API])
        B3([Показать список слотов])
        B4([Отправить выбор в API])
        B5([Показать результат])
    end

    subgraph L3["🟧 Appointments API"]
        A0([Проверить свободен ли слот])
        A1([Создать запись<br/>в БД])
        A2([Вернуть успех<br/>или 409 Conflict])
    end

    subgraph L4["🗄️ PostgreSQL"]
        DB[(appointments<br/>UNIQUE doctor_id+start_time)]
    end

    %% поток
    P0 --> B0 --> P1 --> B1
    B1 --> B2 --> A0 --> DB
    DB -- свободно --> A1 --> DB
    DB --> A2
    A2 -- 201 Created --> B3 --> P2
    P2 --> B4 --> A0
    DB -- свободно? --> A1
    A2 -- 201 Created --> B5 --> P3
    DB -- конфликт --> A2
    A2 -- 409 Conflict --> B3  %% пациент выбирает другое время

    %% стили
    style P0 fill:#f5f5f5,stroke:#999
    style B0 fill:#e0f7fa,stroke:#00acc1
    style A0 fill:#fff8e1,stroke:#ffb300
    style DB fill:#e8eaf6,stroke:#3f51b5
