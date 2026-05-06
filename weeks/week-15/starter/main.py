from fastapi import FastAPI

app = FastAPI()

@app.get("/api/tickets")
def get_tickets():
    return {"status": "ok", "message": "Here are your tickets"}

@app.post("/api/tickets")
def create_ticket():
    return {"status": "created", "id": 123}