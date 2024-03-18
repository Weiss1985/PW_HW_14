from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, PastDate, ConfigDict

from src.schemas.auth import UserResponse


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50, min_length=3)
    second_name: str = Field(max_length=50, min_length=3)
    mail: EmailStr = Field(max_length=60, min_length=6)
    birthday: PastDate
    addition: str = Field(max_length=300) 


class ContactResponse(ContactModel):
    id: int
    first_name: str  
    second_name: str 
    mail: EmailStr  
    birthday: PastDate | None   
    addition: str | None
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None
    model_config =  ConfigDict(from_attributes = True) 



class ContactUpdate(ContactModel):
    first_name: str  
    second_name: str 
    mail: EmailStr  
    birthday: PastDate | None
    addition: str | None
    created_at: datetime | None

    
    

