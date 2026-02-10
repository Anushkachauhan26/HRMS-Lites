from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

# MongoDB connection
MONGO_URL = "mongodb+srv://anushkachauhan369_db_user:anushka197626@employee-cluster.bngqydt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)
db = client["employee_db"]
employee_collection = db["employees"]
attendance_collection = db["attendance"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Employee(BaseModel):
    employeeId: int
    fullName: str
    email: str
    department: str

class Attendance(BaseModel):
    employeeId: int
    date: date  # Pydantic isey validate karega
    status: str

@app.get("/")
def home():
    return {"message": "Employee API with MongoDB is running"}

@app.post("/employees")
def add_employee(emp: Employee):
    if employee_collection.find_one({"employeeId": emp.employeeId}):
        return {"error": "Employee ID already exists"}
    employee_collection.insert_one(emp.dict())
    return {"message": "Employee added successfully"}

@app.get("/employees")
def get_employees():
    return list(employee_collection.find({}, {"_id": 0}))

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    result = employee_collection.delete_one({"employeeId": emp_id})
    if result.deleted_count == 0:
        return {"error": "Employee not found"}
    return {"message": "Employee deleted"}

@app.post("/attendance")
def mark_attendance(record: Attendance):
    if not employee_collection.find_one({"employeeId": record.employeeId}):
        return {"error": "Employee ID not found in database"}
    
    # Convert date to string before saving to avoid BSON errors
    data = record.dict()
    data["date"] = str(data["date"]) 
    
    attendance_collection.insert_one(data)
    return {"message": "Attendance marked successfully"}

@app.get("/attendance/{emp_id}")
def get_attendance(emp_id: int):
    # MongoDB se data nikaal kar list mein convert karein
    records = list(attendance_collection.find({"employeeId": emp_id}, {"_id": 0}))
    return records