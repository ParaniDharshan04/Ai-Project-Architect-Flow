from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectCreate(BaseModel):
    project_name: str
    description: str
    tech_stack: str
    features: str
    installation_steps: str
    extra_notes: Optional[str] = ""
    mode: str = "basic"

class ProjectResponse(BaseModel):
    id: UUID
    user_id: UUID
    project_name: str
    description: str
    tech_stack: str
    features: str
    installation_steps: str
    extra_notes: Optional[str]
    generated_readme: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReadmeResponse(BaseModel):
    readme: str
    project_id: UUID
