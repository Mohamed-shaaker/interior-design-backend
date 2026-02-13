import os
import google.generativeai as genai
from fastapi import APIRouter, Depends, HTTPException
from src.core.supabase import get_supabase
from supabase import Client
# from src.modules.auth.service import get_current_active_user 
from pydantic import BaseModel

router = APIRouter()

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class DesignRequest(BaseModel):
    client_name: str
    description: str

@router.post("/analyze")
async def analyze_design(
    request: DesignRequest, 
    supabase: Client = Depends(get_supabase)
    # current_user = Depends(get_current_active_user) # Keep commented until auth is verified
):
    """Uses Gemini to summarize design needs and saves to Supabase via Bridge."""
    try:
        # 1. Ask Gemini for Intelligence
        prompt = (
            "You are an expert Interior Designer. Analyze the following request and "
    "return a response with these sections: \n"
            "1. STYLE: Recommended interior style.\n"
            "2. COLOR: A 3-color palette.\n"
            "3. TIP: One pro furniture layout tip.\n"
           f"Request: {request.description}"
        )
        response = model.generate_content(prompt)
        ai_text = response.text.strip()

        # 2. Save result to Supabase using the HTTPS Bridge
        analysis_data = {
            "client_name": request.client_name,
            "description": request.description,
            "ai_summary": ai_text,
            "suggested_style": "AI Generated" 
        }
        
        # This replaces the SQLAlchemy session code
        db_response = supabase.table("design_analyses").insert(analysis_data).execute()

        return {"status": "success", "analysis": ai_text, "data": db_response.data}
    except Exception as e:
        print(f"AI Router Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))