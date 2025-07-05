````markdown
<!-- docs/erd.md -->

# ER-диаграмма «Appointments Service»

```mermaid
erDiagram
    APPOINTMENTS {
        INTEGER id PK
        INTEGER doctor_id
        TEXT    patient_name
        TIMESTAMP start_time
    }

    %% если когда-нибудь добавим врачей и пациентов, будут так:
    %% DOCTORS ||--o{ APPOINTMENTS : "doctor_id"
    %% PATIENTS ||--o{ APPOINTMENTS : "patient_id"
````

## Ключевые моменты

* **id** – первичный ключ, auto-increment (SERIAL в Postgres).
* **doctor\_id** – внешний ключ на таблицу врачей в будущей расширенной модели.
* **patient\_name** – строка, хранит ФИО пациента (для простоты, вместо связи на таблицу `patients`).
* **start\_time** – дата и время начала приёма.

### Ограничения

* Составной уникальный индекс `(doctor_id, start_time)` гарантирует, что один врач не сможет вести два приёма в одно время.

```

Сохраните файл под именем **`docs/erd.md`** рядом с исходниками. GitHub отрисует Mermaid-ER диаграмму автоматически.
```
