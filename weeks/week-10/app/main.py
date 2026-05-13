from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class CommentCreate(BaseModel):
    name: str
    author: str

class CommentResponse(CommentCreate):
    id: int
    model_config = {"from_attributes": True}

comments_db: dict[int, dict] = {}
current_id: int = 1

@app.get("/comments", response_model=List[CommentResponse])
def get_comments():
    return list(comments_db.values())

@app.post("/comments", response_model=CommentResponse, status_code=201)
def create_comment(comment: CommentCreate):
    global current_id
    new_comment = {"id": current_id, "name": comment.name, "author": comment.author}
    comments_db[current_id] = new_comment
    current_id += 1
    return new_comment

@app.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int):
    if comment_id not in comments_db:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comments_db[comment_id]

@app.get("/health")
def health():
    return {"status": "healthy"}
