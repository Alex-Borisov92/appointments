CREATE TABLE IF NOT EXISTS appointments (
    id          SERIAL PRIMARY KEY,
    doctor_id   INTEGER NOT NULL,
    patient_name TEXT    NOT NULL,
    start_time  TIMESTAMP NOT NULL,
    CONSTRAINT uq_doctor_time UNIQUE (doctor_id, start_time)
);
