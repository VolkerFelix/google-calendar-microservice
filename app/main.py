import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config.settings import settings
from app.api.routes import router as api_router

# Initialize FastAPI app
def create_application() -> FastAPI:
    app = FastAPI(
        title="Google Calendar Microservice",
        description="A microservice for interacting with Google Calendar API",
        version=settings.VERSION,
        docs_url="/docs" if settings.SHOW_DOCS else None,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify the allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router)

    @app.get("/")
    async def root():
        """Root endpoint to check if the service is running."""
        return {"message": "Google Calendar Microservice is running"}

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app

app = create_application()