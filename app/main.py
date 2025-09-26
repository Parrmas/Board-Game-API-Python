import os
from pathlib import Path
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.core.config import settings

# Import database connection functions
try:
    from app.core.database.connection import connect_to_mongo, close_mongo_connection
except ImportError:
    # Allow project to run even if dependencies not installed yet
    connect_to_mongo = close_mongo_connection = lambda: None

API_URL = os.getenv("API_URL", "")

# --- Lifespan event handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

# --- Create main API router with prefix ---
api_router = APIRouter(prefix="/api")

# --- Health Check Route ---
@api_router.get("/health")
def health_check():
    return {"status": "ok"}


# --- FastAPI App ---
servers_config = []
if settings.API_URL:
    servers_config = [{"url": settings.API_URL, "description": "API base URL"}]

app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Project"),
    version="1.0.0",
    lifespan=lifespan,
    servers=servers_config
)

# --- Middleware (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Feature Routes (uncomment when ready) ---
# from app.features.users.routes import router as users_router
# from app.features.auth.routes import router as auth_router
# app.include_router(users_router, prefix="/users", tags=["Users"])
# app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# --- Include the router ---
app.include_router(api_router)  # ✅ This mounts all router routes under /api