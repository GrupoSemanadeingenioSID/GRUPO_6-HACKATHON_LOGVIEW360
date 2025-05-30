"""
Merger for combining logs from different sources by transaction ID.
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

from utils.logger import setup_logger
from .secucheck_parser import SecucheckParser
from .midflow_parser import MidflowParser
from .corebank_parser import CorebankParser

logger = setup_logger('merger')

class LogMerger:
    """Merger for combining logs from different sources."""
    
    def __init__(
        self,
        secucheck_path: str,
        midflow_path: str,
        corebank_path: str
    ):
        """
        Initialize the merger.
        
        Args:
            secucheck_path (str): Path to security check logs
            midflow_path (str): Path to middleware flow logs
            corebank_path (str): Path to core banking logs
        """
        self.secucheck_path = secucheck_path
        self.midflow_path = midflow_path
        self.corebank_path = corebank_path
        
    def merge_logs(self) -> pd.DataFrame:
        """
        Merge logs from all sources by transaction ID.
        
        Returns:
            pd.DataFrame: Combined log data
        """
        try:
            # Parse individual logs
            secu_df = SecucheckParser(self.secucheck_path).parse_file()
            mid_df = MidflowParser(self.midflow_path).parse_file()
            core_df = CorebankParser(self.corebank_path).parse_file()
            
            # Start with security checks as base
            merged = secu_df.copy()
            
            # Add middleware flow data
            merged = pd.merge(
                merged,
                mid_df,
                on=['transaction_id', 'user_id', 'ip_address', 'module'],
                how='left',
                suffixes=('_secu', '')
            )
            
            # Add core banking data
            merged = pd.merge(
                merged,
                core_df,
                on=['transaction_id', 'user_id', 'ip_address', 'module'],
                how='left',
                suffixes=('', '_core')
            )
            
            # Add transaction status flags
            merged['has_security_check'] = merged['timestamp_secu'].notna()
            merged['has_middleware_flow'] = merged['service_latency'].notna()
            merged['has_core_banking'] = merged['timestamp_core'].notna()
            
            # Calculate completion percentage
            merged['completion_pct'] = (
                merged[['has_security_check', 'has_middleware_flow', 'has_core_banking']]
                .mean(axis=1) * 100
            )
            
            # Calculate end-to-end latency only for complete flows
            merged['e2e_latency'] = None
            complete_flows = merged['has_security_check'] & merged['has_core_banking']
            if complete_flows.any():
                merged.loc[complete_flows, 'e2e_latency'] = (
                    merged.loc[complete_flows, 'timestamp_core'] - 
                    merged.loc[complete_flows, 'timestamp_secu']
                ).dt.total_seconds()
            
            # Order columns logically
            columns = [
                'transaction_id',
                'timestamp_secu', 'start_time', 'end_time', 'timestamp_core',
                'operation', 'status', 'amount',
                'validation_result', 'failure_reason',
                'service_latency', 'total_latency', 'e2e_latency',
                'verifications',
                'user_id', 'ip_address', 'module',
                'account_type',
                'has_security_check', 'has_middleware_flow', 'has_core_banking',
                'completion_pct'
            ]
            
            # Log merge statistics
            total_txns = len(merged)
            logger.info(f"Total transactions: {total_txns}")
            logger.info(f"With security check: {merged['has_security_check'].sum()} ({merged['has_security_check'].mean()*100:.1f}%)")
            logger.info(f"With middleware flow: {merged['has_middleware_flow'].sum()} ({merged['has_middleware_flow'].mean()*100:.1f}%)")
            logger.info(f"With core banking: {merged['has_core_banking'].sum()} ({merged['has_core_banking'].mean()*100:.1f}%)")
            logger.info(f"Complete flows: {complete_flows.sum()} ({complete_flows.mean()*100:.1f}%)")
            
            return merged[columns]
            
        except Exception as e:
            logger.error(f"Error merging logs: {str(e)}")
            raise 