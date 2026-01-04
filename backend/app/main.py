"""FastAPI main application"""
# Add parent directory to Python path to allow importing engine module
import sys
import os
from pathlib import Path

# Get the backend directory (where this file is located)
BACKEND_DIR = Path(__file__).parent.parent
# Get project root (parent of backend directory)
PROJECT_ROOT = BACKEND_DIR.parent

# Add project root to sys.path if not already there
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api import briefs, usage, dodo, admin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(briefs.router)
app.include_router(usage.router)
app.include_router(dodo.router)
app.include_router(admin.router)

# Include dev router only in development
if settings.environment != "production":
    from app.api import dev
    app.include_router(dev.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

