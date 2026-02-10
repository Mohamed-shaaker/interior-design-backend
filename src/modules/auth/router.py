from fastapi import APIRouter, Depends, HTTPException, status
from src.database import get_supabase
from supabase import Client

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(email: str, password: str, supabase: Client = Depends(get_supabase)):
    """
    Register a new user using the Supabase Auth Bridge.
    """
    try:
        # This handles the hashing and storage for you!
        auth_response = supabase.auth.sign_up({
            "email": email, 
            "password": password
        })
        return {"message": "Registration successful", "user": auth_response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(email: str, password: str, supabase: Client = Depends(get_supabase)):
    """
    Login via the HTTPS Bridge.
    """
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")