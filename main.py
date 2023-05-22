from pydantic import BaseModel
from typing import Dict
from fastapi import FastAPI, HTTPException

app = FastAPI()


class StudentCreateSchema(BaseModel):
    first_name: str
    last_name: str


students: Dict[int, StudentCreateSchema] = {}


@app.post("/student")
async def create_student(student: StudentCreateSchema):
    """
    Endpoint that creates a new student.
    """
    if any(char.isdigit() for char in student.first_name) or any(char.isdigit() for char in student.last_name):
        raise HTTPException(
            status_code=400, detail="Student information cannot contain digits")
    if not student.first_name or not student.last_name:
        raise HTTPException(
            status_code=400, detail="Student information cannot be empty")
    existing_ids = [student_id for student_id, s in students.items(
    ) if s.first_name == student.first_name and s.last_name == student.last_name]
    if len(existing_ids) > 1 or (len(existing_ids) == 1 and existing_ids[0] != id):
        raise HTTPException(
            status_code=400, detail="Duplicate student information")

    student_id = len(students) + 1
    students[student_id] = student
    return {"id": student_id, **student.dict()}


@app.get("/students")
async def list_students():
    """
    Endpoint that lists all students.
    """
    return list(students.values())


class StudentUpdateSchema(BaseModel):
    first_name: str
    last_name: str


@app.get("/student/{id}")
async def get_student(id: int):
    """
    Endpoint that retrieves a student by ID.
    """
    if id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": id, **students[id].dict()}


@app.patch("/student/{id}")
async def update_student(id: int, student: StudentUpdateSchema):
    """
    Endpoint that updates a student's information by ID.
    """
    if id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if any(char.isdigit() for char in student.first_name) or any(char.isdigit() for char in student.last_name):
        raise HTTPException(
            status_code=400, detail="Student information cannot contain digits")
    if not student.first_name or not student.last_name:
        raise HTTPException(
            status_code=400, detail="Student information cannot be empty")
    existing_ids = [student_id for student_id, s in students.items(
    ) if s.first_name == student.first_name and s.last_name == student.last_name]
    if len(existing_ids) > 1 or (len(existing_ids) == 1 and existing_ids[0] != id):
        raise HTTPException(
            status_code=400, detail="Duplicate student information")
    students[id].first_name = student.first_name
    students[id].last_name = student.last_name
    return {"id": id, **students[id].dict()}
