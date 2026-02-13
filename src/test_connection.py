import os
import httpx
from dotenv import load_dotenv
from src.core.supabase import get_supabase

# Load keys
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

async def test_full_system():
    print("🚀 Starting Intelligence Hub System Check...")

    # 1. Test Supabase Bridge
    try:
        db = get_supabase()
        # Just a simple health check to see if we can reach the cloud
        health_check = db.table("leads").select("count", count="exact").limit(1).execute()
        print("✅ Supabase Bridge: Connected (Secure ES256)")
    except Exception as e:
        print(f"❌ Supabase Error: {e}")

    # 2. Test Gemini AI Connection
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json={"contents": [{"parts": [{"text": "Hello"}]}]})
            if res.status_code == 200:
                print("✅ Gemini AI: Connected and Responding")
            else:
                print(f"⚠️ Gemini AI: Status {res.status_code}")
    except Exception as e:
        print(f"❌ AI Connection Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_full_system())