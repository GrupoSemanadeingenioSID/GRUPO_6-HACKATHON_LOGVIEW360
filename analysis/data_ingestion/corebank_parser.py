"""
Parser for core banking logs.
"""
from typing import Dict, List, Optional
import pandas as pd
import re
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger('corebank_parser')

class CorebankParser:
    """Parser for core banking logs."""
    
    def __init__(self, log_path: str):
        """
        Initialize the parser.
        
        Args:
            log_path (str): Path to the core banking log file
        """
        self.log_path = log_path
        
    def parse_line(self, line: str) -> Optional[Dict]:
        """
        Parse a single log line.
        
        Args:
            line (str): Log line to parse
            
        Returns:
            Optional[Dict]: Parsed log entry or None if line is invalid
        """
        try:
            # Example line:
            # 2025-05-13 08:00:10 INFO [mobile] user65@198.81.20.19 Transacción ejecutada (transaction: txn-0000, tipo: consignar, cuenta: ahorros, estado: Completada, valor: 429947.36)
            
            # Extract timestamp and basic info
            match = re.match(
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO \[(.*?)\] (.*?)@(.*?) Transacción ejecutada \((.*?)\)',
                line
            )
            
            if not match:
                return None
                
            timestamp, module, user_id, ip_address, details = match.groups()
            
            # Parse transaction details
            details_dict = {}
            for pair in details.split(', '):
                key, value = pair.split(': ')
                details_dict[key] = value
                
            return {
                'timestamp': timestamp,
                'module': module,
                'user_id': user_id,
                'ip_address': ip_address,
                'transaction_id': details_dict['transaction'],
                'operation': details_dict['tipo'],
                'account_type': details_dict['cuenta'],
                'status': details_dict['estado'],
                'amount': float(details_dict['valor'])
            }
            
        except Exception as e:
            logger.error(f"Error parsing line: {str(e)}")
            return None
            
    def parse_file(self) -> pd.DataFrame:
        """
        Parse the entire log file.
        
        Returns:
            pd.DataFrame: Parsed log data
        """
        try:
            parsed_logs = []
            with open(self.log_path, 'r') as f:
                for line in f:
                    parsed_line = self.parse_line(line.strip())
                    if parsed_line:
                        parsed_logs.append(parsed_line)
            
            df = pd.DataFrame(parsed_logs)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Rename timestamp column
            df = df.rename(columns={'timestamp': 'timestamp_core'})
            
            # Order columns
            columns = [
                'timestamp_core', 'transaction_id', 'operation', 'status',
                'amount', 'account_type', 'user_id', 'ip_address', 'module'
            ]
            
            return df[columns]
            
        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}")
            raise 