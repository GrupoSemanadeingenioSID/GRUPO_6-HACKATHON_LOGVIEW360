"""
Pydantic models for API request/response schemas.
"""
from pydantic import BaseModel
from typing import Dict, Optional, List
from datetime import datetime

class TransactionQuery(BaseModel):
    """Schema for transaction query parameters."""
    transaction_id: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class TransactionTrace(BaseModel):
    """Schema for transaction trace response."""
    transaction_id: str
    flow_path: str
    timestamps: Dict[str, Optional[float]]
    latencies: Dict[str, Optional[float]]
    status: str
    amount: Optional[float]

class AnalysisResponse(BaseModel):
    """Schema for analysis response."""
    timestamp: str
    latency_stats: Dict
    flow_stats: Dict
    anomaly_counts: Dict

class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    last_analysis: Optional[str]

class RefreshResponse(BaseModel):
    """Schema for refresh response."""
    status: str 