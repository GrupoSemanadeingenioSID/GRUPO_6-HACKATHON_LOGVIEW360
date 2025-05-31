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

class DataFieldInfo(BaseModel):
    """Schema for field information."""
    name: str = Field(..., description="Name of the field")
    type: str = Field(..., description="Data type of the field")
    description: str = Field(..., description="Description of the field")
    nullable: bool = Field(..., description="Whether the field can be null")
    example: Optional[str] = Field(None, description="Example value")

class DataStructureResponse(BaseModel):
    """Schema for data structure response."""
    total_fields: int = Field(..., description="Total number of fields in the dataset")
    timestamp_fields: List[DataFieldInfo] = Field(..., description="Timestamp related fields")
    transaction_fields: List[DataFieldInfo] = Field(..., description="Transaction related fields")
    user_fields: List[DataFieldInfo] = Field(..., description="User related fields")
    latency_fields: List[DataFieldInfo] = Field(..., description="Latency related fields")
    status_fields: List[DataFieldInfo] = Field(..., description="Status and validation fields")
    metadata_fields: List[DataFieldInfo] = Field(..., description="Metadata and flag fields")

class TimestampInfo(BaseModel):
    """Schema for timestamp information."""
    security: Optional[str] = Field(None, description="Security check timestamp")
    middleware_start: Optional[str] = Field(None, description="Middleware start timestamp")
    middleware_end: Optional[str] = Field(None, description="Middleware end timestamp")
    core_banking: Optional[str] = Field(None, description="Core banking timestamp")

class ValidationInfo(BaseModel):
    """Schema for validation information."""
    result: Optional[str] = Field(None, description="Validation result")
    failure_reason: Optional[str] = Field(None, description="Reason for failure")
    verifications: List[str] = Field(default_factory=list, description="List of verifications performed")

class LatencyInfo(BaseModel):
    """Schema for latency information."""
    service: Optional[float] = Field(None, description="Service latency in seconds")
    total: Optional[float] = Field(None, description="Total latency in seconds")
    end_to_end: Optional[float] = Field(None, description="End-to-end latency in seconds")

class UserInfo(BaseModel):
    """Schema for user information."""
    user_id: Optional[str] = Field(None, description="User ID")
    ip_address: Optional[str] = Field(None, description="IP address")

class SystemInfo(BaseModel):
    """Schema for system information."""
    module: Optional[str] = Field(None, description="System module")
    account_type: Optional[str] = Field(None, description="Account type")

class FlowStatus(BaseModel):
    """Schema for flow status information."""
    has_security_check: bool = Field(False, description="Whether security check was performed")
    has_middleware_flow: bool = Field(False, description="Whether middleware flow was performed")
    has_core_banking: bool = Field(False, description="Whether core banking was performed")
    completion_percentage: float = Field(0.0, description="Flow completion percentage")

class LogRecord(BaseModel):
    """Schema for a single log record."""
    transaction_id: str = Field(..., description="ID of the transaction")
    timestamps: TimestampInfo = Field(..., description="Timestamps for each stage")
    operation: Optional[str] = Field(None, description="Type of operation")
    status: Optional[str] = Field(None, description="Status of the transaction")
    amount: Optional[float] = Field(None, description="Transaction amount")
    validation: ValidationInfo = Field(..., description="Validation information")
    latencies: LatencyInfo = Field(..., description="Latency information")
    user_info: UserInfo = Field(..., description="User information")
    system_info: SystemInfo = Field(..., description="System information")
    flow_status: FlowStatus = Field(..., description="Flow status information")

class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(10, description="Number of records per page", ge=1, le=100)

class PaginationMetadata(BaseModel):
    """Schema for pagination metadata."""
    total_records: int = Field(..., description="Total number of records")
    total_pages: int = Field(..., description="Total number of pages")
    current_page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of records per page")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")

class LogDataResponse(BaseModel):
    """Schema for log data response."""
    metadata: PaginationMetadata = Field(..., description="Pagination metadata")
    data: List[LogRecord] = Field(..., description="List of log records") 