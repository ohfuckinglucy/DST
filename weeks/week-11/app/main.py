from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

class ItemCreate(BaseModel):
    name: str
    sku: str

class ItemResponse(ItemCreate):
    id: int
    model_config = {"from_attributes": True}

items_db: dict[int, dict] = {}
current_id: int = 1

@app.get("/items", response_model=List[ItemResponse])
def get_items():
    return list(items_db.values())

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    global current_id
    new_item = {"id": current_id, "name": item.name, "sku": item.sku}
    items_db[current_id] = new_item
    current_id += 1
    return new_item

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.get("/health")
def health():
    return {"status": "healthy", "db_host": DB_HOST}
