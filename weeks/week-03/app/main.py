from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

class LogCreate(BaseModel):
    name: str
    level: str

class LogResponse(LogCreate):
    id: int
    model_config = {"from_attributes": True}

logs_db: dict[int, dict] = {}
current_id: int = 1

@app.get("/logs", response_model=List[LogResponse])
def get_logs():
    return list(logs_db.values())

@app.post("/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
def create_log(log: LogCreate):
    global current_id
    new_log = {"id": current_id, "name": log.name, "level": log.level}
    logs_db[current_id] = new_log
    current_id += 1
    return new_log

@app.get("/logs/{log_id}", response_model=LogResponse)
def get_log(log_id: int):
    if log_id not in logs_db:
        raise HTTPException(status_code=404, detail="Log not found")
    return logs_db[log_id]

@app.get("/other", response_model=dict)
def get_other():
    return {"service": "other-mock", "status": "ok"}

@app.post("/other", response_model=dict, status_code=201)
def create_other():
    return {"service": "other-mock", "created": True}