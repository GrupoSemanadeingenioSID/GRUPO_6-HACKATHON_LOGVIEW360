"""
Latency analysis for transaction processing times.
"""
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger('latency_analysis')

class LatencyAnalyzer:
    """Analyzer for transaction processing latencies."""
    
    def __init__(self):
        """Initialize the latency analyzer."""
        pass
        
    def calculate_basic_stats(
        self,
        df: pd.DataFrame,
        latency_cols: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate basic latency statistics.
        
        Args:
            df (pd.DataFrame): Input dataframe
            latency_cols (List[str]): List of latency column names
            
        Returns:
            Dict[str, Dict[str, float]]: Statistics by latency type
        """
        try:
            stats = {}
            
            for col in latency_cols:
                if col in df.columns:
                    stats[col] = {
                        'mean': df[col].mean(),
                        'median': df[col].median(),
                        'std': df[col].std(),
                        'min': df[col].min(),
                        'max': df[col].max(),
                        'p95': df[col].quantile(0.95),
                        'p99': df[col].quantile(0.99)
                    }
                    
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating latency stats: {str(e)}")
            raise
            
    def analyze_by_dimension(
        self,
        df: pd.DataFrame,
        dimension: str,
        latency_col: str = 'service_latency'
    ) -> pd.DataFrame:
        """
        Analyze latencies grouped by a specific dimension.
        
        Args:
            df (pd.DataFrame): Input dataframe
            dimension (str): Column to group by
            latency_col (str): Latency column to analyze
            
        Returns:
            pd.DataFrame: Latency statistics by dimension
        """
        try:
            # Ensure latency column is numeric
            df[latency_col] = pd.to_numeric(df[latency_col], errors='coerce')
            
            # Filter out rows with missing latency values
            valid_df = df[pd.notna(df[latency_col])].copy()
            
            # Log data quality stats
            total_rows = len(df)
            valid_rows = len(valid_df)
            logger.info(f"Analyzing latencies for {latency_col}:")
            logger.info(f"Total rows: {total_rows}")
            logger.info(f"Valid numeric values: {valid_rows} ({valid_rows/total_rows*100:.1f}%)")
            
            # Group by dimension and calculate statistics
            grouped = pd.DataFrame()
            grouped['mean'] = valid_df.groupby(dimension)[latency_col].mean()
            grouped['median'] = valid_df.groupby(dimension)[latency_col].median()
            grouped['std'] = valid_df.groupby(dimension)[latency_col].std()
            grouped['min'] = valid_df.groupby(dimension)[latency_col].min()
            grouped['max'] = valid_df.groupby(dimension)[latency_col].max()
            grouped['p95'] = valid_df.groupby(dimension)[latency_col].quantile(0.95)
            grouped['p99'] = valid_df.groupby(dimension)[latency_col].quantile(0.99)
            grouped['count'] = valid_df.groupby(dimension)[latency_col].count()
            
            # Round numeric columns to 3 decimal places
            numeric_cols = ['mean', 'median', 'std', 'min', 'max', 'p95', 'p99']
            grouped[numeric_cols] = grouped[numeric_cols].round(3)
            
            return grouped
            
        except Exception as e:
            logger.error(f"Error analyzing latencies by dimension: {str(e)}")
            raise
            
    def analyze_trends(
        self,
        df: pd.DataFrame,
        latency_col: str,
        window: str = '5min'
    ) -> pd.DataFrame:
        """
        Analyze latency trends over time.
        
        Args:
            df (pd.DataFrame): Input dataframe
            latency_col (str): Name of latency column to analyze
            window (str): Time window for rolling calculations
            
        Returns:
            pd.DataFrame: Trend analysis results
        """
        try:
            # Sort by timestamp
            df = df.sort_values('timestamp_secu')
            
            # Calculate rolling statistics
            trends = pd.DataFrame()
            trends['timestamp'] = df['timestamp_secu']
            trends['latency'] = df[latency_col]
            trends['rolling_mean'] = df[latency_col].rolling(window=window).mean()
            trends['rolling_std'] = df[latency_col].rolling(window=window).std()
            trends['rolling_max'] = df[latency_col].rolling(window=window).max()
            
            # Calculate trend indicators
            trends['trend'] = trends['rolling_mean'].diff().fillna(0)
            trends['volatility'] = (
                trends['rolling_std'] / trends['rolling_mean']
            ).fillna(0)
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            raise
            
    def find_bottlenecks(
        self,
        df: pd.DataFrame,
        threshold_percentile: float = 95
    ) -> pd.DataFrame:
        """
        Identify bottlenecks in transaction processing.
        
        Args:
            df (pd.DataFrame): Input dataframe
            threshold_percentile (float): Percentile to use for thresholds
            
        Returns:
            pd.DataFrame: Identified bottlenecks
        """
        try:
            bottlenecks = []
            
            # Analyze service latency
            if 'service_latency' in df.columns:
                service_threshold = df['service_latency'].quantile(threshold_percentile/100)
                service_bottlenecks = df[df['service_latency'] > service_threshold]
                
                for _, txn in service_bottlenecks.iterrows():
                    bottlenecks.append({
                        'transaction_id': txn['transaction_id'],
                        'stage': 'MIDDLEWARE',
                        'latency': txn['service_latency'],
                        'threshold': service_threshold,
                        'operation': txn['operation'],
                        'module': txn['module']
                    })
                    
            # Analyze end-to-end latency
            if 'e2e_latency' in df.columns:
                e2e_threshold = df['e2e_latency'].quantile(threshold_percentile/100)
                e2e_bottlenecks = df[df['e2e_latency'] > e2e_threshold]
                
                for _, txn in e2e_bottlenecks.iterrows():
                    bottlenecks.append({
                        'transaction_id': txn['transaction_id'],
                        'stage': 'END_TO_END',
                        'latency': txn['e2e_latency'],
                        'threshold': e2e_threshold,
                        'operation': txn['operation'],
                        'module': txn['module']
                    })
                    
            return pd.DataFrame(bottlenecks)
            
        except Exception as e:
            logger.error(f"Error finding bottlenecks: {str(e)}")
            raise 