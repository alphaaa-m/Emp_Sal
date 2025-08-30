from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime

from fastapi import APIRouter
from schemas.atd_sch import AttendanceCreate
from models.emp import Employee
from models.atd import Attendance
from database.db import get_db
from models.sal import Salary

router = APIRouter(
    prefix="/atd",
    tags=["atd"],
)


@router.post("/attendance/")
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    # Check if a base salary record exists for the month
    base_salary_record = db.query(Salary).filter(
        Salary.employee_id == attendance.employee_id,
        Salary.month == attendance.date.strftime("%Y-%m"),
        Salary.is_base_salary == True
    ).first()

    if not base_salary_record:
        return {"error": "Base salary record not found for this employee and month. Cannot track attendance salary."}

    # Calculate the daily rate
    days_in_month = (attendance.date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    daily_rate = base_salary_record.amount / days_in_month.day

    # Update calculated salary based on attendance status
    if attendance.status.lower() in ["present", "leave"]:
        base_salary_record.calculated_salary += daily_rate
        if attendance.status.lower() == "leave":
            employee = db.query(Employee).filter(Employee.id == attendance.employee_id).first()
            if employee:
                employee.total_leaves += 1

    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    db.refresh(base_salary_record)

    return {
        "attendance": db_attendance,
        "updated_calculated_salary": round(base_salary_record.calculated_salary, 2)
    }

@router.get("/attendance/")
def read_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()
