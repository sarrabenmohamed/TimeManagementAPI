from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    name: str
    role: str | None = None

class EmployeeUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
