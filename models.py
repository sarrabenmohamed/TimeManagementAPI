import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)  # <-- integer primary key
    name = Column(String, index=True)
    role = Column(String, nullable=True)
    shifts = relationship("WorkShift", back_populates="employee", cascade="all, delete-orphan")


class WorkShift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    employee = relationship("Employee", back_populates="shifts")


