from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.leads.schemas import LeadCreate, LeadResponse
from src.modules.leads.service import LeadService
from src.api.dependencies import get_db

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_in: LeadCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint for landing page form submissions.
    """
    service = LeadService(db)
    return await service.create_lead(lead_in)

@router.get("/", response_model=list[LeadResponse])
async def get_all_leads(
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint for the Admin Dashboard to see all submissions.
    """
    service = LeadService(db)
    return await service.get_all_leads()