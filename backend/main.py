from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
from pathlib import Path

from backend.database import connect_to_mongo, close_mongo_connection, init_default_tenant
from backend.routes import chat, widget, auth, leads, knowledge_base
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    await connect_to_mongo()
    await init_default_tenant()
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    logger.info(f"LeadPilot AI started in {settings.environment} mode")
    logger.info(f"Backend URL: {settings.backend_url}")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    
    yield
    
    # Shutdown
    await close_mongo_connection()
    print("👋 LeadPilot AI shutting down")


# Create FastAPI app
app = FastAPI(
    title="LeadPilot AI",
    description="Autonomous Lead Qualification System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://localhost:3000",
        "*"  # Allow all origins for widget embedding
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(widget.router)
app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(knowledge_base.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Mount static files for frontend
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    # Mount assets directory (JS, CSS, images)
    assets_path = frontend_dist / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
    
    # Serve widget files
    widget_path = Path(__file__).parent.parent / "frontend" / "public" / "widget"
    if widget_path.exists():
        app.mount("/widget", StaticFiles(directory=str(widget_path)), name="widget")
    
    # Catch-all route for React Router (must be last)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend for all non-API routes"""
        # Don't serve frontend for API routes
        if full_path.startswith("v1/") or full_path == "docs" or full_path == "openapi.json" or full_path == "redoc":
            return {"error": "Not found"}
        
        # Serve index.html for all other routes (React Router handles routing)
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"error": "Frontend not built. Run 'npm run build' in frontend directory."}
else:
    print("⚠️  Frontend dist folder not found. Run 'npm run build' in frontend directory.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    )
