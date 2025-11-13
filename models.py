from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, nullable=True)

class WorkShift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

