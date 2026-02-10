import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("https://uguungxnrzzxqixikbhn.supabase.co")
key = os.environ.get("sb_publishable_rZiy7HJe1C4tSoAli05DUA_DYsiIZcB")
supabase = create_client(url, key)

try:
    # This uses standard HTTPS (Port 443) which isn't blocked!
    response = supabase.table("users").select("*").execute()
    print("✅ SUCCESS: We bypassed the firewall using the Bridge!")
except Exception as e:
    print(f"❌ Bridge failed: {e}")