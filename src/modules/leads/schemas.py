from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class LeadBase(BaseModel):
    email: EmailStr
    # IMPORTANT: Changed from fullName to full_name to match the Database Model
    full_name: str 
    project_type: Optional[str] = None
    description: str

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)