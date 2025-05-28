from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.hash import bcrypt
from db import db

router = APIRouter()

class UserAuth(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: UserAuth):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_pw = bcrypt.hash(user.password)
    result = db.users.insert_one({
        "email": user.email,
        "password": hashed_pw
    })

    return {"msg": "User registered", "user_id": str(result.inserted_id)}

@router.post("/login")
def login(user: UserAuth):
    record = db.users.find_one({"email": user.email})
    if not record or not bcrypt.verify(user.password, record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"msg": "Login successful", "user_id": str(record["_id"])}
