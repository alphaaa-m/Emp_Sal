from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime


# DATABASE_URL = "postgresql://postgres:ayeshamuneeb786@db.zbulhomqbaghzgwxuxjy.supabase.co:5432/postgres?sslmode=require"
DATABASE_URL = "postgresql://postgres.zbulhomqbaghzgwxuxjy:ayeshamuneeb786@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()