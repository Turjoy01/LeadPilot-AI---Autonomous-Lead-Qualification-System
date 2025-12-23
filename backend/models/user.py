from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    full_name: str
    tenant_id: str
    role: str = "admin"  # admin, sales_rep, viewer
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserInDB(User):
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    
    model_config = ConfigDict(populate_by_name=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    tenant_id: str
    role: str = "admin"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    tenant_id: Optional[str] = None
