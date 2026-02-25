from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    due: str

class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True

tasks_db: dict[int, dict] = {}
current_id: int = 1

@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    """
    GET /tasks — вернуть список всех объектов.
    """
    return list(tasks_db.values())

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """
    POST /tasks — создать новый объект.
    """
    global current_id
    
    new_task = {
        "id": current_id,
        "title": task.title,
        "due": task.due,
    }
    
    tasks_db[current_id] = new_task
    
    current_id += 1
    
    return new_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    """
    GET /tasks/{id} — получить один объект по его ID.
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    
    return tasks_db[task_id]