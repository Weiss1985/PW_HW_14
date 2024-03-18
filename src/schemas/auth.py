from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate, ConfigDict

from src.database.models import Role


class UserModel(BaseModel):
    username: str = Field(max_length=50, min_length=3)
    mail: EmailStr = Field(max_length=60, min_length=6)
    password: str = Field(min_length=4, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    mail: EmailStr
    avatar: str | None
    # created_at: datetime
    role: Role | None
    model_config=  ConfigDict(from_attributes = True) 


class UsertUpdate(UserModel):
    first_name: str  
    second_name: str 
    mail: EmailStr  
    birthday: PastDate 
    addition: str | None
    role: Role | None
    created_at: datetime

    
class TokenModel(BaseModel):
    access_token: str 
    refresh_token: str 
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    mail: EmailStr  




