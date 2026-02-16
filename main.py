from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- ROUTER IMPORTS ---
from src.modules.leads.router import router as leads_router
from src.modules.auth.router import router as auth_router
# NOTE: If ai_router still uses 'get_db', the app might crash. 
# We can comment it out temporarily if you haven't fixed src/modules/ai/router.py yet.
from src.modules.ai.router import router as ai_router

app = FastAPI(
    title="Interior Design API",
   
)

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTER ROUTERS ---

app.include_router(auth_router)
app.include_router(leads_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    return {
        "status": "online", 
        "message": "Backend is Running via HTTPS Bridge 🌉",
        "docs": "/docs"
    }