from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.modules.leads.router import router as leads_router
from src.modules.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for startup/shutdown events.
    This runs once when the server starts and once when it stops.
    """
    print("Startup: Creating database tables...")
    async with engine.begin() as conn: 
        # This line automatically creates tables in Postgres based on your Models
        await conn.run_sync(Base.metadata.create_all)
    print("Startup: Tables created successfully.")
    
    yield
    
    print("Shutdown: Closing database connection...")
    await engine.dispose()

# --- CRITICAL: These lines MUST be at the very edge (Zero Indentation) ---
# This makes the 'app' variable visible to the Uvicorn server.

app = FastAPI(
    title="Interior Design API",
    version="1.0.0",
    lifespan=lifespan
)

# --- CORS CONFIGURATION (The Bridge) ---
# This allows your local HTML file (usually on port 5500) to talk to port 8000
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*" # For development, allows any connection
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering our domain modules
app.include_router(leads_router)
app.include_router(auth_router)