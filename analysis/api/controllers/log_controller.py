"""
Controllers for handling API endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from ..services.log_service import LogService
from ..models.schemas import (
    TransactionTrace, 
    AnalysisResponse, 
    HealthCheck, 
    RefreshResponse,
    BottleneckDetail,
    BottleneckSummary,
    TimeRangeQuery,
    LatencyTrend
)
from utils.logger import setup_logger

logger = setup_logger('controller')

class LogController:
    def __init__(self, service: LogService):
        """Initialize controller with service."""
        self.service = service
        self.router = APIRouter(prefix="/api/v1", tags=["logs"])
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

        @self.router.get("/bottlenecks", response_model=List[BottleneckDetail])
        async def get_bottlenecks(
            query: TimeRangeQuery = Depends(),
        ) -> List[BottleneckDetail]:
            """
            Get detailed information about bottlenecks within a time range.
            
            Args:
                query: Time range and filtering parameters
                
            Returns:
                List of bottleneck details
            """
            try:
                return self.service.get_bottlenecks(query)
            except Exception as e:
                logger.error(f"Error getting bottlenecks: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.get("/bottlenecks/summary", response_model=BottleneckSummary)
        async def get_bottlenecks_summary(
            start_time: Optional[datetime] = Query(None),
            end_time: Optional[datetime] = Query(None),
        ) -> BottleneckSummary:
            """
            Get a summary of bottleneck statistics.
            
            Args:
                start_time: Optional start of time range
                end_time: Optional end of time range
                
            Returns:
                Summary statistics about bottlenecks
            """
            try:
                return self.service.get_bottlenecks_summary(start_time, end_time)
            except Exception as e:
                logger.error(f"Error getting bottlenecks summary: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.get("/bottlenecks/trends", response_model=List[LatencyTrend])
        async def get_latency_trends(
            window: str = Query("5min", description="Time window for aggregation (e.g. 5min, 1h)"),
            last_hours: int = Query(24, ge=1, le=168, description="Number of hours to analyze"),
        ) -> List[LatencyTrend]:
            """
            Get latency trends over time.
            
            Args:
                window: Time window for aggregation
                last_hours: Number of past hours to analyze
                
            Returns:
                List of latency trends by time window
            """
            try:
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=last_hours)
                return self.service.get_latency_trends(start_time, end_time, window)
            except Exception as e:
                logger.error(f"Error getting latency trends: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e)) 