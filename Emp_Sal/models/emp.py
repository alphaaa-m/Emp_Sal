from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime
from database.db import Base





class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_of_joining = Column(Date, default=datetime.date.today)
    total_leaves = Column(Integer, default=0)

    salaries = relationship("Salary", back_populates="employee")
    attendance = relationship("Attendance", back_populates="employee")