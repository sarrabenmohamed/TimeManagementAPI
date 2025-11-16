from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.employee import EmployeeCreate, EmployeeUpdate
from models import Employee
from database import get_db

router = APIRouter()

@router.post("/")
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(Employee).filter(Employee.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee with this name already exists")

    employee = Employee(name=data.name, role=data.role)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.id == employee_id).first()

@router.get("/")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.put("/{employee_id}")
def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(404, "Employee not found")

    if payload.name is not None:
        employee.name = payload.name
    if payload.role is not None:
        employee.role = payload.role

    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(404, "Employee not found")

    db.delete(employee)
    db.commit()
