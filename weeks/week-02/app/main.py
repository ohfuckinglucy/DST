from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class ProfileCreate(BaseModel):
    name: str
    phone: str

class ProfileResponse(ProfileCreate):
    id: int
    
    model_config = {"from_attributes": True}

profiles_db: dict[int, dict] = {}
current_id: int = 1

# GET - получает список профилей
@app.get("/profiles", response_model=List[ProfileResponse])
def get_all_profiles():
    return list(profiles_db.values())

# POST - жобалвяет в список профилей
@app.post("/profiles", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileCreate):
    global current_id
    
    new_profile = {
        "id": current_id,
        "name": profile.name,
        "phone": profile.phone,
    }
    
    profiles_db[current_id] = new_profile
    current_id += 1
    
    return new_profile

# GET - получает по индексу
@app.get("/profiles/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int):
    if profile_id not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Profile with id {profile_id} not found"
        )
    return profiles_db[profile_id]

# PUT - меняет по индексу
@app.put("/profiles/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, profile_update: ProfileCreate):
    if profile_id not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Profile with id {profile_id} not found for update"
        )
    
    updated_profile = {
        "id": profile_id,
        "name": profile_update.name,
        "phone": profile_update.phone,
    }
    
    profiles_db[profile_id] = updated_profile
    return updated_profile

# DELETE - удаляет по индексу
@app.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int):
    if profile_id not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Profile with id {profile_id} not found for deletion"
        )
    
    del profiles_db[profile_id]
    return None