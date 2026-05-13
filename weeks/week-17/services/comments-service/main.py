from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Comments Service", version="1.0.0")

class CommentCreate(BaseModel):
    author: str
    text: str

class CommentResponse(CommentCreate):
    id: int
    model_config = {"from_attributes": True}

db: dict[int, dict] = {}
counter: int = 1

@app.get("/comments", response_model=List[CommentResponse])
def list_comments():
    return list(db.values())

@app.post("/comments", response_model=CommentResponse, status_code=201)
def create_comment(payload: CommentCreate):
    global counter
    record = {"id": counter, "author": payload.author, "text": payload.text}
    db[counter] = record
    counter += 1
    return record

@app.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int):
    if comment_id not in db:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db[comment_id]

@app.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, payload: CommentCreate):
    if comment_id not in db:
        raise HTTPException(status_code=404, detail="Comment not found")
    db[comment_id] = {"id": comment_id, "author": payload.author, "text": payload.text}
    return db[comment_id]

@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int):
    if comment_id not in db:
        raise HTTPException(status_code=404, detail="Comment not found")
    del db[comment_id]

@app.get("/health")
def health():
    return {"status": "healthy", "service": "comments-s19"}
