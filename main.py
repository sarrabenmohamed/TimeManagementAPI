from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import employee, shifts

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router, prefix="/employees", tags=["Employees"])
app.include_router(shifts.router, prefix="/shifts", tags=["Shifts"])
