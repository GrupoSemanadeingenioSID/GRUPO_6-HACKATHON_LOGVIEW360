"""
Repository for handling log data operations.
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple, List, Optional

from data_ingestion.merger import LogMerger
from processing.normalizer import LogNormalizer
from processing.latency_analysis import LatencyAnalyzer
from processing.flow_mapper import FlowMapper
from utils.logger import setup_logger
from utils.config import SOURCE_DIR

logger = setup_logger('repository')

class LogRepository:
    def __init__(self):
        """Initialize repository with data processors."""
        self.merger = LogMerger(
            secucheck_path=f"{SOURCE_DIR}/logs_SecuCheck.json",
            midflow_path=f"{SOURCE_DIR}/logs_MidFlow_ESB.csv",
            corebank_path=f"{SOURCE_DIR}/logs_CoreBank.log"
        )
        self.normalizer = LogNormalizer()
        self.latency_analyzer = LatencyAnalyzer()
        self.flow_mapper = FlowMapper()
        
        # Cache
        self._data: Optional[pd.DataFrame] = None
        self._last_update: Optional[datetime] = None
        
    def get_data(self, force_refresh: bool = False) -> pd.DataFrame:
        """Get the normalized log data."""
        if force_refresh or self._data is None:
            self.refresh_data()
        return self._data
    
    def refresh_data(self) -> None:
        """Refresh the log data."""
        try:
            df = self.merger.merge_logs()
            self._data = self.normalizer.normalize_dataframe(df)
            self._last_update = datetime.now()
        except Exception as e:
            logger.error(f"Error refreshing data: {str(e)}")
            raise
            
    def get_transaction(self, transaction_id: str) -> Tuple[pd.DataFrame, List[str], List[float]]:
        """Get transaction data and its flow."""
        df = self.get_data()
        transaction = df[df['transaction_id'] == transaction_id]
        
        if transaction.empty:
            return None, [], []
            
        flow, timestamps = self.flow_mapper.map_transaction_flow(df, transaction_id)
        return transaction, flow, timestamps
    
    def get_analysis_stats(self) -> Dict:
        """Get analysis statistics."""
        df = self.get_data()
        
        # Calculate statistics
        latency_stats = self.latency_analyzer.calculate_basic_stats(
            df, ['service_latency', 'total_latency', 'e2e_latency']
        )
        
        # Analyze flows
        flow_patterns, flow_stats = self.flow_mapper.analyze_flow_patterns(df)
        flow_anomalies = self.flow_mapper.detect_anomalies(df)
        
        # Count anomalies by type
        pattern_anomalies = len(flow_anomalies[flow_anomalies['anomaly_types'].apply(
            lambda x: any('INCOMPLETE_FLOW' in t or 'MISSING_STAGES' in t for t in x)
        )])
        sequence_anomalies = len(flow_anomalies[flow_anomalies['anomaly_types'].apply(
            lambda x: 'LONG_DURATION' in x
        )])
        
        return {
            'latency_stats': latency_stats,
            'flow_stats': flow_stats,
            'anomaly_counts': {
                'pattern': pattern_anomalies,
                'sequence': sequence_anomalies,
                'bottlenecks': len(self.latency_analyzer.find_bottlenecks(df))
            }
        }
    
    def get_last_update(self) -> Optional[datetime]:
        """Get the timestamp of the last data update."""
        return self._last_update 