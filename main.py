from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Employee(BaseModel):
    name: str
    department: str
    salary: int

conn = psycopg2.connect(
    database="employee_directory",
    user="postgres",
    password="Krishna@2003",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


@app.get("/")
def home():
    return {"message": "Employee Directory API"}


@app.get("/employees")
def get_employees():

    cur.execute("SELECT * FROM employees")

    rows = cur.fetchall()
    # print(rows)

    result = []

    for row in rows:

        result.append(
            {
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "salary": row[3]
            }
        )

    return result


@app.post("/employees")
def add_employee(employee: Employee):

    cur.execute(
        """
        INSERT INTO employees
        (employee_name, department, salary)
        VALUES (%s, %s, %s)
        """,
        (
            employee.name,
            employee.department,
            employee.salary
        )
    )

    conn.commit()

    return {"message": "Employee Added Successfully"}

@app.get("/employees/search/{name}")
def search_employee(name: str):

    cur.execute(
        """
        SELECT * FROM employees
        WHERE employee_name ILIKE %s
        """,
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append(
            {
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "salary": row[3]
            }
        )

    return result

@app.get("/employees/department/{department}")
def filter_department(department: str):

    cur.execute(
        """
        SELECT * FROM employees
        WHERE department ILIKE %s
        """,
        (department,)
    )

    rows = cur.fetchall()

    result = []

    for row in rows:
        result.append(
            {
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "salary": row[3]
            }
        )

    return result


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    cur.execute(
        """
        DELETE FROM employees
        WHERE employee_id = %s
        """,
        (employee_id,)
    )

    conn.commit()

    return {
        "message": "Employee deleted"
    }


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: dict
):

    cur.execute(
        """
        UPDATE employees
        SET employee_name=%s,
            department=%s,
            salary=%s
        WHERE employee_id=%s
        """,
        (
            employee["name"],
            employee["department"],
            employee["salary"],
            employee_id
        )
    )

    conn.commit()

    return {
        "message": "Employee updated"
    }