from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Users Service", version="1.0.0")

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(UserCreate):
    id: int
    model_config = {"from_attributes": True}

db: dict[int, dict] = {}
counter: int = 1

@app.get("/users", response_model=List[UserResponse])
def list_users():
    return list(db.values())

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    global counter
    record = {"id": counter, "name": payload.name, "email": payload.email}
    db[counter] = record
    counter += 1
    return record

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]

@app.get("/health")
def health():
    return {"status": "healthy", "service": "users-s19"}
