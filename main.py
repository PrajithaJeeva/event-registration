from fastapi import FastAPI
from database import init_db, get_connection

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

import sqlite3
from datetime import datetime
from fastapi import HTTPException

MAX_CAPACITY = 50

app = FastAPI()
init_db()

class RegistrationIn(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    college: Optional[str] = None

@app.get("/")
def home():
    return {"message": "Server is running"}

@app.post("/register", status_code=201)
def register(data: RegistrationIn):
    conn = get_connection()

    cursor = conn.execute("SELECT COUNT(*) FROM registrations")
    count = cursor.fetchone()[0]
    if count >= MAX_CAPACITY:
        conn.close()
        raise HTTPException(
                             status_code=409,
                             detail="Event Is Full"
        )
        
        
    time_now = datetime.now().isoformat()
    
    try:
     conn.execute(
         "INSERT INTO registrations (name, email, college, registered_at) VALUES (?, ?, ?, ?)",
    (data.name, data.email, data.college, time_now)

     )
    except sqlite3.IntegrityError:
       conn.close()
       raise HTTPException(
                            status_code=409,
                            detail="Already registered"
                )

    conn.commit()
    conn.close()

    return {"message": "Registered successfully", "name": data.name, "email": data.email}

@app.get("/registrations")
def get_all_registrations():
    conn = get_connection()

    cursor = conn.execute("SELECT * FROM registrations")
    rows = cursor.fetchall()
    conn.close()

    students = [dict(row) for row in rows]

    return students

@app.get("/registrations/{registration_id}")
def get_registration(registration_id: int):
    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM registrations WHERE id = ?",
        (registration_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None :
        raise HTTPException(
            status_code = 404,
            detail = "Registration Not Found"
        )
    return dict(row)