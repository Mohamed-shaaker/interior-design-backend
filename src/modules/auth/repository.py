from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.models import User
from src.modules.auth.schemas import UserCreate

class UserRepository:
    def __init__(self, session: AsyncSession):
        """
        Injected database session. 
        As per standards, the Repository does NOT commit transactions.
        """
        self.session = session

    async def create(self, user_in: UserCreate, hashed_password: str) -> User:
        """
        Creates a new user record.
        The actual save to the physical disk happens when the Service calls .commit()
        """
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False
        )
        self.session.add(db_user)
        return db_user

    async def get_by_email(self, email: str) -> User | None:
        """
        Queries the database for a user with the specific email.
        Returns the User object if found, or None if not.
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()