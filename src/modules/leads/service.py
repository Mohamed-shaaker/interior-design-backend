from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.leads.repository import LeadRepository
from src.modules.leads.schemas import LeadCreate
from src.modules.leads.models import Lead

class LeadService:
    def __init__(self, db: AsyncSession):
        self.repository = LeadRepository(db)
        self.db = db

    async def create_lead(self, lead_in: LeadCreate) -> Lead:
        """
        Business logic for creating a lead.
        """
        new_lead = await self.repository.create(lead_in)
        await self.db.commit()
        await self.db.refresh(new_lead)
        return new_lead

    async def get_all_leads(self) -> list[Lead]:
        """
        Business logic for retrieving all leads.
        """
        return await self.repository.get_all()