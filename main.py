from typing import Union

from sqlalchemy.orm import Session

from models import Employee, WorkShift
from database import *
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic schemas
class EmployeeCreate(BaseModel):
    name: str
    role: str | None = None

class ShiftCreate(BaseModel):
    employee_id: int
    start_time: datetime
    end_time: datetime

# CRUD for employees
@app.post("/employees/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(name=employee.name, role=employee.role)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# CRUD for shifts
@app.post("/shifts/")
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    # Validate employee exists
    if not db.query(Employee).filter(Employee.id == shift.employee_id).first():
        raise HTTPException(status_code=404, detail="Employee not found")
    # Validate no overlapping shift
    overlapping = db.query(WorkShift).filter(
        WorkShift.employee_id == shift.employee_id,
        WorkShift.start_time < shift.end_time,
        WorkShift.end_time > shift.start_time
    ).first()
    if overlapping:
        raise HTTPException(status_code=400, detail="Shift overlaps with existing shift")
    db_shift = WorkShift(
        employee_id=shift.employee_id,
        start_time=shift.start_time,
        end_time=shift.end_time
    )
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

#TODO add delete and update endpoints