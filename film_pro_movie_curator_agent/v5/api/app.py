from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from api.routers import router

app =  FastAPI(
    title="FilmPro AI",
    description="Movie recommendations agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ====== ROUTERS =====
app.include_router(router)

# ====== HEALTH CHECK ENDPOINT =====
# You typically declare endpoints directly on @app when they are global, system-level endpoints that don't belong to any specific feature or business logic.

@app.get(
    "/health",
    tags=["system"],
    summary="Check API health",
    description="Returns API state"
)
async def health_check():
    """
    Healthcheck endpoint to check if app is up.
    """
    return {
        "status": "ok",
        "service": "FilmPro API",
        "version": "1.0.0"
    }
    
    
@app.get(
    "/",
    tags=["system"],
    summary="API Information",
    description="Gets information about API FilmPro"
)
async def root():
    """
    Root endpoint with API information.
    """
    
    return {
        "name": "FilmPro API",
        "description": "Film recommendation API based on AI Agent",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "recommendations": "/recommendations",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
    
