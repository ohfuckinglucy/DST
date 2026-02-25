from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class MessageCreate(BaseModel):
    name: str
    topic: str

class MessageResponse(MessageCreate):
    id: int
    
    model_config = {"from_attributes": True}

messages_db: dict[int, dict] = {}
current_id: int = 1

# GET /messages возвращает список всех обьектов.
@app.get("/messages", response_model=List[MessageResponse])
def get_all_messages():
    return list(messages_db.values())

# POST /messages создает новый объект.
@app.post("/messages", response_model=MessageResponse, status_code=201)
def create_message(message: MessageCreate):
    global current_id
    
    new_message = {
        "id": current_id,
        "name": message.name,
        "topic": message.topic,
    }
    
    messages_db[current_id] = new_message
    current_id += 1
    
    return new_message

# GET /messages/{id} получает обьект по его id
@app.get("/messages/{message_id}", response_model=MessageResponse)
def get_message_by_id(message_id: int):
    if message_id not in messages_db:
        raise HTTPException(status_code=404, detail=f"Message with id {message_id} not found")
    
    return messages_db[message_id]