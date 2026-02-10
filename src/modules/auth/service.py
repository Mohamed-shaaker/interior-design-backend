from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db
from src.core.security import SECRET_KEY, ALGORITHM, get_password_hash, verify_password
from src.modules.auth.repository import UserRepository
from src.modules.auth.schemas import UserCreate
from src.modules.auth.models import User

# This defines how the frontend sends the token (as a Bearer token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.db = db

    async def register_new_user(self, user_in: UserCreate) -> User:
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise Exception("A user with this email already exists.")
        hashed_password = get_password_hash(user_in.password)
        new_user = await self.repository.create(user_in, hashed_password)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

# --- THE MISSING BOUNCER FUNCTION ---
async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repo = UserRepository(db)
    user = await repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user