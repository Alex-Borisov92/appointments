from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentBase(BaseModel):
    doctor_id: int = Field(..., gt=0)
    patient_name: str
    start_time: datetime


class AppointmentCreate(AppointmentBase):
    """Схема входящего запроса (POST /appointments)."""

    pass


class AppointmentRead(AppointmentBase):
    """Схема ответа, возвращаемого клиенту."""

    id: int

    # Pydantic v2: включаем режим ORM-сериализации
    model_config = ConfigDict(from_attributes=True)
