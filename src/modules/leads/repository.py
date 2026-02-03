from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.leads.models import Lead
from src.modules.leads.schemas import LeadCreate

class LeadRepository:
    def __init__(self, session: AsyncSession):
        """
        Injected database session.
        The Repository handles atomic data operations.
        """
        self.session = session
        
    async def create(self, lead_create: LeadCreate) -> Lead:
        """
        Creates a new Lead instance in the session.
        Mapping the Pydantic schema to the SQLAlchemy model.
        """
        db_lead = Lead(
            full_name=lead_create.full_name,
            email=lead_create.email,
            project_type=lead_create.project_type,
            description=lead_create.description
        )
        
        self.session.add(db_lead)
        return db_lead

    async def get_all(self) -> list[Lead]:
        """
        Fetches all leads from the database, ordered by newest first.
        Essential for the upcoming Admin Dashboard.
        """
        query = select(Lead).order_by(Lead.id.desc())
        result = await self.session.execute(query)
        # .scalars() turns the row objects into Lead model objects
        return list(result.scalars().all())