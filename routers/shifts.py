from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.shift import ShiftCreate, ShiftUpdate, ShiftRead
from models import WorkShift, Employee
from database import get_db

router = APIRouter()


@router.post("/")
def create_shift(data: ShiftCreate, db: Session = Depends(get_db)):
    if not db.query(Employee).filter(Employee.id == data.employee_id).first():
        raise HTTPException(404, "Employee not found")

    overlapping = db.query(WorkShift).filter(
        WorkShift.employee_id == data.employee_id,
        WorkShift.start_time < data.end_time,
        WorkShift.end_time > data.start_time
    ).first()

    if overlapping:
        raise HTTPException(400, "Shift overlaps with existing shift")

    shift = WorkShift(**data.dict())
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.get("/{employee_id}", response_model=list[ShiftRead])
def list_shifts(employee_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(WorkShift, Employee).join(Employee, Employee.id == WorkShift.employee_id)

    if employee_id:
        query = query.filter(WorkShift.employee_id == employee_id)

    results = query.all()

    return [
        ShiftRead(
            id=shift.id,
            employee_id=shift.employee_id,
            employee_name=emp.name,
            start_time=shift.start_time,
            end_time=shift.end_time,
        )
        for shift, emp in results
    ]


@router.put("/{shift_id}")
def update_shift(shift_id: int, payload: ShiftUpdate, db: Session = Depends(get_db)):
    shift = db.query(WorkShift).filter(WorkShift.id == shift_id).first()
    if not shift:
        raise HTTPException(404, "Shift not found")

    new_employee = payload.employee_id or shift.employee_id
    new_start = payload.start_time or shift.start_time
    new_end = payload.end_time or shift.end_time

    overlap = db.query(WorkShift).filter(
        WorkShift.employee_id == new_employee,
        WorkShift.id != shift_id,
        WorkShift.start_time < new_end,
        WorkShift.end_time > new_start
    ).first()

    if overlap:
        raise HTTPException(400, "Updated shift overlaps with another shift")

    shift.employee_id = new_employee
    shift.start_time = new_start
    shift.end_time = new_end

    db.commit()
    db.refresh(shift)
    return shift


@router.delete("/{shift_id}", status_code=204)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(WorkShift).filter(WorkShift.id == shift_id).first()
    if not shift:
        raise HTTPException(404, "Shift not found")

    db.delete(shift)
    db.commit()
