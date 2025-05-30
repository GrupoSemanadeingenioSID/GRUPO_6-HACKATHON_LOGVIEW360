"""
Parser for middleware flow logs.
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger('midflow_parser')

class MidflowParser:
    """Parser for middleware flow logs."""
    
    def __init__(self, log_path: str):
        """
        Initialize the parser.
        
        Args:
            log_path (str): Path to the middleware flow log file
        """
        self.log_path = log_path
        
    def parse_file(self) -> pd.DataFrame:
        """
        Parse the entire log file.
        
        Returns:
            pd.DataFrame: Parsed log data with request-response pairs
        """
        try:
            # Read CSV file
            df = pd.read_csv(self.log_path)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Create separate dataframes for requests and responses
            requests = df[df['direction'] == 'request'].copy()
            responses = df[df['direction'] == 'response'].copy()
            
            # Rename timestamp columns before merge
            requests = requests.rename(columns={'timestamp': 'start_time'})
            responses = responses.rename(columns={'timestamp': 'end_time'})
            
            # Merge requests and responses on transaction_id
            merged = pd.merge(
                requests,
                responses,
                on=['transaction_id', 'operation', 'user_id', 'ip_address', 'modulo'],
                suffixes=('_req', '_resp')
            )
            
            # Calculate total latency
            merged['total_latency'] = (
                merged['end_time'] - merged['start_time']
            ).dt.total_seconds()
            
            # Clean up and rename columns
            merged = merged.rename(columns={
                'status_code_resp': 'status_code',
                'modulo': 'module',
                'latency_ms_resp': 'latency_ms'  # La latencia está en la fila de respuesta
            })
            
            # Convert service latency to seconds
            merged['service_latency'] = merged['latency_ms'] / 1000
            
            # Select and order columns
            columns = [
                'transaction_id', 'start_time', 'end_time', 'operation',
                'status_code', 'service_latency', 'total_latency',
                'user_id', 'ip_address', 'module'
            ]
            
            return merged[columns]
            
        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}")
            raise 