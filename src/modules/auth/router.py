from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.schemas import UserCreate, UserResponse
from src.modules.auth.service import AuthService
from src.api.dependencies import get_db
from src.core.security import create_access_token
from datetime import timedelta

# Create the router with a prefix to keep main.py clean
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to register a new admin or user.
    Calls the AuthService to handle hashing and database persistence.
    """
    auth_service = AuthService(db)
    try:
        return await auth_service.register_new_user(user_in)
    except Exception as e:
        # If the user already exists, the service raises an exception
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    The standard login endpoint.
    It receives 'username' and 'password' from the login form,
    verifies them, and returns a JWT access token.
    """
    auth_service = AuthService(db)
    
    # form_data.username is used by OAuth2 standards (we treat it as email)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the digital 'key card' (Token)
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }