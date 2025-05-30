"""
Normalizer for standardizing fields across log sources.
"""
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger('normalizer')

class LogNormalizer:
    """Normalizer for standardizing log fields."""
    
    def __init__(self):
        """Initialize the normalizer."""
        # Standard mappings for modules
        self.module_mapping = {
            'mobile': 'MOBILE',
            'web': 'WEB',
            'api': 'API'
        }
        
        # Standard mappings for operations
        self.operation_mapping = {
            'consignar': 'DEPOSIT',
            'retirar': 'WITHDRAWAL',
            'transferir': 'TRANSFER'
        }
        
        # Standard mappings for status
        self.status_mapping = {
            'Completada': 'COMPLETED',
            'Fallida': 'FAILED',
            'Aprobada': 'APPROVED',
            'Rechazada': 'REJECTED'
        }
        
        # Standard mappings for account types
        self.account_mapping = {
            'ahorros': 'SAVINGS',
            'corriente': 'CHECKING'
        }
        
    def normalize_ip(self, df: pd.DataFrame, ip_col: str = 'ip_address') -> pd.DataFrame:
        """
        Normalize IP addresses to standard format.
        
        Args:
            df (pd.DataFrame): Input dataframe
            ip_col (str): Name of IP address column
            
        Returns:
            pd.DataFrame: DataFrame with normalized IPs
        """
        try:
            # Ensure IP addresses are in standard format (no leading zeros)
            df[ip_col] = df[ip_col].apply(
                lambda x: '.'.join(str(int(i)) for i in x.split('.'))
            )
            return df
        except Exception as e:
            logger.error(f"Error normalizing IPs: {str(e)}")
            raise
            
    def normalize_timestamps(
        self,
        df: pd.DataFrame,
        timestamp_cols: List[str]
    ) -> pd.DataFrame:
        """
        Normalize timestamps to UTC.
        
        Args:
            df (pd.DataFrame): Input dataframe
            timestamp_cols (List[str]): List of timestamp column names
            
        Returns:
            pd.DataFrame: DataFrame with normalized timestamps
        """
        try:
            for col in timestamp_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.tz_localize('UTC')
            return df
        except Exception as e:
            logger.error(f"Error normalizing timestamps: {str(e)}")
            raise
            
    def normalize_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize categorical fields to standard values.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: DataFrame with normalized categorical values
        """
        try:
            # Normalize modules
            if 'module' in df.columns:
                df['module'] = df['module'].map(self.module_mapping)
                
            # Normalize operations
            if 'operation' in df.columns:
                df['operation'] = df['operation'].map(self.operation_mapping)
                
            # Normalize status
            if 'status' in df.columns:
                df['status'] = df['status'].map(self.status_mapping)
                
            # Normalize account types
            if 'account_type' in df.columns:
                df['account_type'] = df['account_type'].map(self.account_mapping)
                
            return df
        except Exception as e:
            logger.error(f"Error normalizing categorical fields: {str(e)}")
            raise
            
    def normalize_numeric(
        self,
        df: pd.DataFrame,
        numeric_cols: List[str]
    ) -> pd.DataFrame:
        """
        Normalize numeric fields (scaling, handling outliers).
        
        Args:
            df (pd.DataFrame): Input dataframe
            numeric_cols (List[str]): List of numeric column names
            
        Returns:
            pd.DataFrame: DataFrame with normalized numeric values
        """
        try:
            for col in numeric_cols:
                if col in df.columns:
                    # Handle outliers using IQR method
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    
                    # Cap outliers at boundaries
                    df[f'{col}_raw'] = df[col].copy()  # Keep raw values
                    df[col] = df[col].clip(lower=lower, upper=upper)
                    
                    # Add outlier flag
                    df[f'{col}_is_outlier'] = (
                        (df[f'{col}_raw'] < lower) | (df[f'{col}_raw'] > upper)
                    )
                    
            return df
        except Exception as e:
            logger.error(f"Error normalizing numeric fields: {str(e)}")
            raise
            
    def normalize_dataframe(
        self,
        df: pd.DataFrame,
        numeric_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Apply all normalizations to a dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
            numeric_cols (List[str], optional): List of numeric columns to normalize
            
        Returns:
            pd.DataFrame: Fully normalized DataFrame
        """
        try:
            # Make a copy to avoid modifying original
            df = df.copy()
            
            # Normalize timestamps
            timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower()]
            df = self.normalize_timestamps(df, timestamp_cols)
            
            # Normalize IP addresses
            df = self.normalize_ip(df)
            
            # Normalize categorical fields
            df = self.normalize_categorical(df)
            
            # Normalize numeric fields if specified
            if numeric_cols:
                df = self.normalize_numeric(df, numeric_cols)
                
            return df
            
        except Exception as e:
            logger.error(f"Error in full normalization: {str(e)}")
            raise 