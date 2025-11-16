from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ShiftCreate(BaseModel):
    employee_id: int
    start_time: datetime
    end_time: datetime

class ShiftUpdate(BaseModel):
    employee_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

class ShiftRead(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)

