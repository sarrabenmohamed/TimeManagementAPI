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

class ShiftUpdate(BaseModel):
    employee_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class EmployeeUpdate(BaseModel):
    name: str | None = None
    role: str | None = None

# CRUD for employees
@app.post("/employees/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(name=employee.name, role=employee.role)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.id == employee_id).first()

@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return
@app.put("/employees/{employee_id}", status_code=200)
def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # update only provided fields
    if payload.name is not None:
        employee.name = payload.name
    if payload.role is not None:
        employee.role = payload.role

    db.commit()
    db.refresh(employee)
    return employee
@app.get("/employees/")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

#----------------------------------------------------------------------------#
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

@app.delete("/shifts/{shift_id}", status_code=204)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(WorkShift).filter(WorkShift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    db.delete(shift)
    db.commit()
    return

@app.delete("/employees/{employee_id}/shifts", status_code=204)
def delete_all_shifts(employee_id: int, db: Session = Depends(get_db)):
    shifts = db.query(WorkShift).filter(WorkShift.employee_id == employee_id).all()
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this employee")

    for s in shifts:
        db.delete(s)

    db.commit()
    return
@app.put("/shifts/{shift_id}", status_code=200)
def update_shift(shift_id: int, payload: ShiftUpdate, db: Session = Depends(get_db)):
    shift = db.query(WorkShift).filter(WorkShift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    # Update only provided fields
    if payload.employee_id is not None:
        shift.employee_id = payload.employee_id
    if payload.start_time is not None:
        shift.start_time = payload.start_time
    if payload.end_time is not None:
        shift.end_time = payload.end_time

    db.commit()
    db.refresh(shift)
    return shift
