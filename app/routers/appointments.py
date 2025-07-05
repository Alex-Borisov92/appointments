# app/routers/appointments.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import get_db  # зависимость для получения Session
from ..models import Appointment
from ..schemas import AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appt: AppointmentCreate,
    db: Session = Depends(get_db),
) -> Appointment:
    """Создать новую запись к врачу.

    Возвращает объект модели Appointment (FastAPI
    сериализует его в AppointmentRead). Если слот занят,
    поднимает 409 Conflict.
    """
    obj = Appointment(**appt.model_dump())
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="slot already taken")
    return obj


@router.get("/{appt_id}", response_model=AppointmentRead)
def get_appointment(appt_id: int, db: Session = Depends(get_db)) -> Appointment:
    """Получить запись по ID. 404 — если запись не найдена."""
    obj = db.get(Appointment, appt_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="appointment not found")
    return obj
