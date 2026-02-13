import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def get_supabase() -> Client:
    if not url or not key:
        raise ValueError("Supabase credentials missing from .env")
    return create_client(url, key)