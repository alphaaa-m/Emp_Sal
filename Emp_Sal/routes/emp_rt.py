from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime

from fastapi import APIRouter
from schemas.emp_sch import EmployeeCreate
from models.emp import Employee
from models.sal import Salary
from database.db import get_db

router = APIRouter(
    prefix="/emp",
    tags=["emp"],
)


@router.post("/employees/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()



@router.get("/employees/salary_summary/")
def get_all_employees_with_salary(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    
    summary = []
    current_month = datetime.date.today().strftime("%Y-%m")
    
    for employee in employees:
        base_salary_record = db.query(Salary).filter(
            Salary.employee_id == employee.id,
            Salary.month == current_month,
            Salary.is_base_salary == True
        ).first()

        summary.append({
            "employee_id": employee.id,
            "employee_name": employee.name,
            "base_salary_this_month": base_salary_record.amount if base_salary_record else "N/A",
            "current_calculated_salary": round(base_salary_record.calculated_salary, 2) if base_salary_record else "N/A"
        })
        
    return summary