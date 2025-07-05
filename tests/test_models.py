from app.models import Appointment


def test_model_fields():
    appt = Appointment(doctor_id=2, patient_name="X", start_time="2030-01-01T11:00:00")
    assert appt.doctor_id == 2
