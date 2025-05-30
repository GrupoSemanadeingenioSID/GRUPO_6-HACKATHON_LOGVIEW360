"""
Controllers for handling API endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict

from ..services.log_service import LogService
from ..models.schemas import TransactionTrace, AnalysisResponse, HealthCheck, RefreshResponse
from utils.logger import setup_logger

logger = setup_logger('controller')

class LogController:
    def __init__(self, service: LogService):
        """Initialize controller with service."""
        self.service = service
        self.router = APIRouter()
        self._setup_routes()
        
    def _setup_routes(self):
        """Set up API routes."""
        
        @self.router.get("/")
        async def root():
            """Root endpoint returning API status."""
            return {"status": "running", "service": "LogView360 API"}
            
        @self.router.get("/health")
        async def health_check() -> HealthCheck:
            """Health check endpoint."""
            last_update = self.service.repository.get_last_update()
            return HealthCheck(
                status="healthy",
                last_analysis=last_update.isoformat() if last_update else None
            )
            
        @self.router.get("/transaction/{transaction_id}/trace")
        async def get_transaction_trace(transaction_id: str) -> TransactionTrace:
            """Get the complete trace of a transaction."""
            try:
                trace = self.service.get_transaction_trace(transaction_id)
                if trace is None:
                    raise HTTPException(status_code=404, detail="Transaction not found")
                return trace
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error processing transaction trace: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
                
        @self.router.get("/metrics/latency")
        async def get_latency_metrics(background_tasks: BackgroundTasks) -> AnalysisResponse:
            """Get system-wide latency metrics."""
            try:
                metrics, needs_refresh = self.service.get_analysis_metrics()
                
                if needs_refresh:
                    background_tasks.add_task(self.service.repository.refresh_data)
                    
                return metrics
            except Exception as e:
                logger.error(f"Error getting latency metrics: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
                
        @self.router.post("/analysis/refresh")
        async def force_refresh(background_tasks: BackgroundTasks) -> RefreshResponse:
            """Force a refresh of the analysis data."""
            try:
                background_tasks.add_task(self.service.repository.refresh_data)
                return RefreshResponse(status="refresh scheduled")
            except Exception as e:
                logger.error(f"Error scheduling refresh: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e)) 