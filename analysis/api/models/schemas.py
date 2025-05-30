"""
Pydantic models for API request/response schemas.
"""
from pydantic import BaseModel, Field
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

class BottleneckDetail(BaseModel):
    """Schema for detailed bottleneck information."""
    transaction_id: str = Field(..., description="ID of the transaction")
    stage: str = Field(..., description="Stage where bottleneck occurred")
    latency: float = Field(..., description="Measured latency")
    threshold: float = Field(..., description="Threshold that was exceeded")
    operation: str = Field(..., description="Operation type")
    module: str = Field(..., description="Module where bottleneck occurred")

class BottleneckSummary(BaseModel):
    """Schema for bottleneck summary statistics."""
    total_bottlenecks: int = Field(..., description="Total number of bottlenecks detected")
    by_stage: Dict[str, int] = Field(..., description="Bottlenecks count by stage")
    by_operation: Dict[str, int] = Field(..., description="Bottlenecks count by operation")
    by_module: Dict[str, int] = Field(..., description="Bottlenecks count by module")
    avg_latency: Dict[str, float] = Field(..., description="Average latency by stage")
    threshold_exceeded: Dict[str, float] = Field(..., description="Average threshold exceedance by stage")

class TimeRangeQuery(BaseModel):
    """Schema for time range query parameters."""
    start_time: Optional[datetime] = Field(None, description="Start of time range")
    end_time: Optional[datetime] = Field(None, description="End of time range")
    module: Optional[str] = Field(None, description="Filter by specific module")
    operation: Optional[str] = Field(None, description="Filter by specific operation")
    limit: Optional[int] = Field(10, description="Maximum number of results to return", ge=1, le=100)

class LatencyTrend(BaseModel):
    """Schema for latency trend analysis."""
    timestamp: datetime
    avg_latency: float
    percentile_95: float
    percentile_99: float
    num_bottlenecks: int 