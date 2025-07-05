from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get():
    data = {"doctor_id": 1, "patient_name": "Test", "start_time": "2030-01-01T10:00:00"}
    r = client.post("/appointments", json=data)
    assert r.status_code == 201
    appt = r.json()
    r2 = client.get(f"/appointments/{appt['id']}")
    assert r2.status_code == 200
    assert r2.json()["doctor_id"] == 1
