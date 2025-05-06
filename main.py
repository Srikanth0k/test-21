from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import datetime
from typing import List
from fastapi import Query

app = FastAPI()

# PostgreSQL connection details
conn = psycopg2.connect(
    dbname="ShopTalk",
    user="postgres",
    password="chicken",
    host="localhost",
    port="5432"
)

class Student(BaseModel):
    name: str
    age: int
    grade: str
    enrolled_date: datetime.date

@app.post("/add_student/")
def add_student(student: Student):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT add_student(%s, %s, %s, %s)",
            (student.name, student.age, student.grade, student.enrolled_date)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return {"message": "Student added", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/grade/{grade}")
def get_student_by_grade(grade: str):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.getstudent_by_grade(%s)", (grade,))
        rows = cursor.fetchall()
        cursor.close()

        students = []
        for row in rows:
            students.append({
                "name": row[0],
                "age": row[1],
                "grade": row[2],
                "enrolled_date": row[3]
            })

        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/enrolled_after/{enrolled_date}")
def get_students_after(enrolled_after: datetime.date = Query(..., description="Date in YYYY-MM-DD format")):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.get_students_after_date(%s)", (enrolled_after,))
        rows = cursor.fetchall()
        cursor.close()

        students = []
        for row in rows:
            students.append({
                "name": row[0],
                "age": row[1],
                "grade": row[2],
                "enrolled_date": row[3]
            })

        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
