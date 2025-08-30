from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime

from fastapi import APIRouter
from models.sal import Salary
from models.atd import Attendance
from database.db import get_db

router = APIRouter(
    prefix="/sal_cal",
    tags=["sal_cal"],
)



@router.get("/salaries/final/{employee_id}/{month}")
def get_final_salary(employee_id: int, month: str, db: Session = Depends(get_db)):
    """
    Returns the final calculated salary for an employee for a given month.
    """
    final_salary_record = db.query(Salary).filter(
        Salary.employee_id == employee_id,
        Salary.month == month,
        Salary.is_base_salary == True
    ).first()

    if not final_salary_record:
        return {"error": "Final salary record not found for this employee and month"}

    return {
        "employee_id": employee_id,
        "month": month,
        "final_salary": round(final_salary_record.calculated_salary, 2)
    }
