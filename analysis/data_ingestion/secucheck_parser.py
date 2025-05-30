"""
Parser for security check logs.
"""
from typing import Dict, List, Optional
import pandas as pd
import json
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger('secucheck_parser')

class SecucheckParser:
    """Parser for security check logs."""
    
    def __init__(self, log_path: str):
        """
        Initialize the parser.
        
        Args:
            log_path (str): Path to the security check log file
        """
        self.log_path = log_path
        
    def parse_file(self) -> pd.DataFrame:
        """
        Parse the entire log file.
        
        Returns:
            pd.DataFrame: Parsed log data
        """
        try:
            with open(self.log_path, 'r') as f:
                logs = json.load(f)
                
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(logs)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Normalize column names
            df = df.rename(columns={
                'resultado_validación': 'validation_result',
                'motivo_fallo': 'failure_reason',
                'módulo': 'module',
                'verificaciones_realizadas': 'verifications',
                'timestamp': 'timestamp_secu'
            })
            
            # Convert verifications list to string for easier processing
            df['verifications'] = df['verifications'].apply(lambda x: ','.join(x))
            
            return df
            
        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}")
            raise 