from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime
from fastapi import APIRouter
from sqlalchemy.sql import func

from database.db import get_db
from schemas.sal_sch import SalaryCreate
from models.sal import Salary


router = APIRouter(
    prefix="/salary",
    tags=["salary"],
)


@router.post("/salaries/")
def create_salary(salary: SalaryCreate, db: Session = Depends(get_db)):
    db_salary = Salary(**salary.dict())
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary

@router.get("/salaries/")
def read_salaries(db: Session = Depends(get_db)):
    return db.query(Salary).all()


@router.get("/salaries/budget_overview/{month}")
def get_monthly_budget(month: str, db: Session = Depends(get_db)):
    total_budget = db.query(func.sum(Salary.calculated_salary)).filter(
        Salary.month == month,
        Salary.is_base_salary == True
    ).scalar()
    
    if total_budget is None:
        total_budget = 0.0

    return {
        "month": month,
        "total_calculated_salary_budget": round(total_budget, 2)
    }