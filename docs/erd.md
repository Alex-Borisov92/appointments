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
