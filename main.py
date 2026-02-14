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
    # We removed 'lifespan' because we don't need to check DB connections on startup anymore.
    # The 'Bridge' connects automatically when a request is made.
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
# Since your routers (like leads_router) already have prefix="/leads" inside them,
# we don't need to add it again here, or we'd get "/leads/leads/..."
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