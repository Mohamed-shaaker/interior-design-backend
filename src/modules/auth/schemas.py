from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

# Note: These are NOT indented. They stand alone.
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    # We will add timestamps to the model next, for now keeping it simple
    
    model_config = ConfigDict(from_attributes=True)