from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.repository import UserRepository
from src.modules.auth.schemas import UserCreate
from src.modules.auth.models import User
from src.core.security import get_password_hash, verify_password

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.db = db

    async def register_new_user(self, user_in: UserCreate) -> User:
        """
        Registers a new user by hashing their password before saving.
        """
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise Exception("A user with this email already exists.")

        # Hash the plain text password from the schema
        hashed_password = get_password_hash(user_in.password)

        new_user = await self.repository.create(user_in, hashed_password)
        
        # We commit here because the Service manages the transaction boundary
        await self.db.commit()
        await self.db.refresh(new_user)
        
        return new_user

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Checks if a user exists and if the provided password matches the hash.
        """
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        
        # Verify the typed password against the stored hash
        if not verify_password(password, user.hashed_password):
            return None
            
        return user