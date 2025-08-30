from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func
import datetime
from database.db import Base



class Salary(Base):
    __tablename__ = "salaries"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    month = Column(String)  # e.g. "2025-08"
    amount = Column(Float)
    calculated_salary = Column(Float, default=0.0)
    is_base_salary = Column(Boolean, default=True)

    employee = relationship("Employee", back_populates="salaries")