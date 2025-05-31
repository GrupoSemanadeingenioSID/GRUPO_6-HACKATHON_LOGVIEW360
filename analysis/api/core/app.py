"""
Main FastAPI application configuration.
"""
from fastapi import FastAPI
import uvicorn

from ..controllers.log_controller import LogController
from ..services.log_service import LogService
from ..repositories.log_repository import LogRepository
from utils.config import API_HOST, API_PORT

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="LogView360 API",
        description="API for analyzing and viewing log data",
        version="1.0.0"
    )
    
    # Set up dependency injection
    repository = LogRepository()
    service = LogService(repository)
    controller = LogController(service)
    
    # Include routes
    app.include_router(controller.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    ) 