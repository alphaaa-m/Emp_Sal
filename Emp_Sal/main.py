from fastapi import FastAPI
from database.db import engine
from routes import atd_rt,sal_cal_rt, emp_rt,sal_rt
from models import sal, emp, atd
from database.db import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
                title="Employee Salary",
                description="""Welcome..!""",
                version="1.0.0",
                license_info={"name": "Muneeb Ashraf"})



@app.get("/")
def home():
    return {"message": "Welcome"}



app.include_router(emp_rt.router)
app.include_router(atd_rt.router)
app.include_router(sal_rt.router)
app.include_router(sal_cal_rt.router)
