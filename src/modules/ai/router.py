import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.core.supabase import get_supabase
from supabase import Client
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])

class DesignRequest(BaseModel):
    client_name: str
    description: str

@router.post("/analyze")
async def analyze_design(request: DesignRequest, supabase: Client = Depends(get_supabase)):
    api_key = os.getenv("GEMINI_API_KEY")
    # Using the stable v1 URL to ensure no more 404s
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        # 1. The Design Brain Instructions
        prompt = f"You are a Senior Interior Designer. Analyze this: {request.description}. Provide STYLE, PALETTE, and one TIP."
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=20.0)
            
            if response.status_code != 200:
                return {"error": "Google API Error", "details": response.json()}

            data = response.json()
            ai_text = data['candidates'][0]['content']['parts'][0]['text']

        # 2. Save to Supabase
        # Note: Ensure your table is named 'design_analyses'
        supabase.table("design_analyses").insert({
            "client_name": request.client_name,
            "description": request.description,
            "ai_summary": ai_text
        }).execute()

        return {"status": "success", "analysis": ai_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))