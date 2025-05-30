"""
Service layer for handling business logic.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional, Tuple

from ..repositories.log_repository import LogRepository
from ..models.schemas import TransactionTrace, AnalysisResponse
from utils.logger import setup_logger

logger = setup_logger('service')

class LogService:
    def __init__(self, repository: LogRepository):
        """Initialize service with repository."""
        self.repository = repository
        self.CACHE_DURATION_SECONDS = 300  # 5 minutes
        
    def needs_refresh(self) -> bool:
        """Check if data needs refresh."""
        last_update = self.repository.get_last_update()
        if not last_update:
            return True
        return (datetime.now() - last_update).total_seconds() > self.CACHE_DURATION_SECONDS
        
    def get_transaction_trace(self, transaction_id: str) -> TransactionTrace:
        """Get transaction trace with validation."""
        transaction, flow, timestamps = self.repository.get_transaction(transaction_id)
        
        if transaction is None:
            return None
            
        # Validar y limpiar timestamps
        valid_timestamps = {}
        for stage, ts in zip(flow, timestamps):
            try:
                if pd.isna(ts) or np.isinf(ts):
                    logger.warning(f"Invalid timestamp for stage {stage} in transaction {transaction_id}")
                    valid_timestamps[stage] = None
                else:
                    valid_timestamps[stage] = float(ts)
            except Exception as e:
                logger.warning(f"Error processing timestamp for stage {stage}: {str(e)}")
                valid_timestamps[stage] = None
        
        # Validar latencias
        latencies = {}
        for metric in ['service_latency', 'total_latency', 'e2e_latency']:
            try:
                value = transaction[metric].iloc[0]
                if pd.isna(value) or np.isinf(value):
                    logger.warning(f"Invalid {metric} for transaction {transaction_id}")
                    latencies[metric] = None
                else:
                    latencies[metric] = float(value)
            except Exception as e:
                logger.warning(f"Error processing {metric}: {str(e)}")
                latencies[metric] = None
        
        # Validar amount
        try:
            amount = transaction['amount'].iloc[0]
            if pd.isna(amount) or np.isinf(amount):
                logger.warning(f"Invalid amount for transaction {transaction_id}")
                amount = None
            else:
                amount = float(amount)
        except Exception as e:
            logger.warning(f"Error processing amount: {str(e)}")
            amount = None
            
        # Validar status
        try:
            status = transaction['status'].iloc[0]
            if pd.isna(status):
                logger.warning(f"Invalid status for transaction {transaction_id}")
                status = "UNKNOWN"
        except Exception as e:
            logger.warning(f"Error processing status: {str(e)}")
            status = "UNKNOWN"
            
        return TransactionTrace(
            transaction_id=transaction_id,
            flow_path="->".join(flow) if flow else "",
            timestamps=valid_timestamps,
            latencies=latencies,
            status=status,
            amount=amount
        )
        
    def get_analysis_metrics(self, force_refresh: bool = False) -> Tuple[AnalysisResponse, bool]:
        """Get analysis metrics and refresh status."""
        needs_refresh = force_refresh or self.needs_refresh()
        
        if needs_refresh:
            self.repository.refresh_data()
            
        stats = self.repository.get_analysis_stats()
        last_update = self.repository.get_last_update()
        
        return (
            AnalysisResponse(
                timestamp=last_update.isoformat(),
                **stats
            ),
            needs_refresh
        ) 