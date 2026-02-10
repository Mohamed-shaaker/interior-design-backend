import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# This is your new 'engine'
supabase: Client = create_client(url, key)

def get_supabase():
    return supabase

if __name__ == "__main__":
    try:
        # Simple health check to prove the tunnel is open
        response = supabase.table("users").select("count", count="exact").execute()
        print("✅ CONNECTION SUCCESSFUL: The HTTPS Tunnel is open!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")