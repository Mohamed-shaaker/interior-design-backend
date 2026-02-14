from fastapi import APIRouter, Depends, HTTPException, status
from src.modules.leads.schemas import LeadCreate, LeadResponse
from src.core.supabase import get_supabase
from supabase import Client

# Note: We removed 'LeadService' and 'get_db' because they use the blocked connection.

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead_in: LeadCreate, 
    supabase: Client = Depends(get_supabase)
):
    """
    Public Endpoint: Submits a lead via the HTTPS Bridge.
    """
    try:
        # Convert Pydantic model to a standard Python dictionary
        lead_data = lead_in.model_dump()
        
        # Insert into Supabase 'leads' table
        # .execute() returns a response object with 'data' inside
        response = supabase.table("leads").insert(lead_data).execute()
        
        # Supabase returns a list of inserted rows. We want the first one.
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=400, detail="Supabase insert failed")
            
    except Exception as e:
        # If the table doesn't exist or schema is wrong, this catches it
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[LeadResponse])
def get_all_leads(
    supabase: Client = Depends(get_supabase)
):
    """
    Admin Endpoint: Fetches all leads via the HTTPS Bridge.
    """
    try:
        response = supabase.table("leads").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))