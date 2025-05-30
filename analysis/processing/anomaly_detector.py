"""
Anomaly detection for transaction logs.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from datetime import datetime, timedelta

from utils.logger import setup_logger
from utils.config import LATENCY_THRESHOLD, ANOMALY_SCORE_THRESHOLD

logger = setup_logger('anomaly_detector')

class AnomalyDetector:
    """Detector for anomalies in transaction logs."""
    
    def __init__(self):
        """Initialize the anomaly detector."""
        # Initialize models
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
        self.lof = LocalOutlierFactor(
            contamination=0.1,
            novelty=True
        )
        
        self.scaler = StandardScaler()
        
    def detect_latency_anomalies(
        self,
        df: pd.DataFrame,
        latency_cols: List[str],
        threshold_percentile: float = 95
    ) -> pd.DataFrame:
        """
        Detect anomalous latencies using statistical and ML methods.
        
        Args:
            df (pd.DataFrame): Input dataframe
            latency_cols (List[str]): Latency columns to analyze
            threshold_percentile (float): Percentile for statistical threshold
            
        Returns:
            pd.DataFrame: DataFrame with anomaly scores
        """
        try:
            anomalies = []
            
            for col in latency_cols:
                if col not in df.columns:
                    continue
                    
                # Statistical detection
                threshold = df[col].quantile(threshold_percentile/100)
                statistical_anomalies = df[df[col] > threshold]
                
                for _, txn in statistical_anomalies.iterrows():
                    anomalies.append({
                        'transaction_id': txn['transaction_id'],
                        'anomaly_type': 'HIGH_LATENCY',
                        'metric': col,
                        'value': txn[col],
                        'threshold': threshold,
                        'detection_method': 'STATISTICAL',
                        'score': (txn[col] - df[col].mean()) / df[col].std()
                    })
                    
            return pd.DataFrame(anomalies)
            
        except Exception as e:
            logger.error(f"Error detecting latency anomalies: {str(e)}")
            raise
            
    def detect_pattern_anomalies(
        self,
        df: pd.DataFrame,
        features: List[str]
    ) -> pd.DataFrame:
        """
        Detect anomalous patterns using machine learning.
        
        Args:
            df (pd.DataFrame): Input dataframe
            features (List[str]): Feature columns for anomaly detection
            
        Returns:
            pd.DataFrame: DataFrame with anomaly scores
        """
        try:
            # Prepare feature matrix
            X = df[features].fillna(0)
            X_scaled = self.scaler.fit_transform(X)
            
            # Train models
            self.isolation_forest.fit(X_scaled)
            self.lof.fit(X_scaled)
            
            # Get predictions
            if_scores = self.isolation_forest.score_samples(X_scaled)
            lof_scores = self.lof.score_samples(X_scaled)
            
            # Combine results
            anomalies = []
            
            for idx, (if_score, lof_score) in enumerate(zip(if_scores, lof_scores)):
                if if_score < ANOMALY_SCORE_THRESHOLD or lof_score < ANOMALY_SCORE_THRESHOLD:
                    txn = df.iloc[idx]
                    anomalies.append({
                        'transaction_id': txn['transaction_id'],
                        'anomaly_type': 'PATTERN_ANOMALY',
                        'if_score': if_score,
                        'lof_score': lof_score,
                        'detection_method': 'ML'
                    })
                    
            return pd.DataFrame(anomalies)
            
        except Exception as e:
            logger.error(f"Error detecting pattern anomalies: {str(e)}")
            raise
            
    def detect_sequence_anomalies(
        self,
        df: pd.DataFrame,
        time_window: timedelta = timedelta(minutes=5)
    ) -> pd.DataFrame:
        """
        Detect anomalies in transaction sequences.
        
        Args:
            df (pd.DataFrame): Input dataframe
            time_window (timedelta): Time window for sequence analysis
            
        Returns:
            pd.DataFrame: DataFrame with sequence anomalies
        """
        try:
            anomalies = []
            
            # Sort by timestamp
            df = df.sort_values('timestamp_secu')
            
            # Group transactions by user
            for user_id, user_df in df.groupby('user_id'):
                # Check transaction frequency
                for i in range(len(user_df) - 1):
                    current = user_df.iloc[i]
                    next_txn = user_df.iloc[i + 1]
                    
                    time_diff = next_txn['timestamp_secu'] - current['timestamp_secu']
                    
                    # Check for suspiciously rapid sequences
                    if time_diff < timedelta(seconds=1):
                        anomalies.append({
                            'transaction_id': next_txn['transaction_id'],
                            'anomaly_type': 'RAPID_SEQUENCE',
                            'user_id': user_id,
                            'time_diff': time_diff.total_seconds(),
                            'detection_method': 'SEQUENCE'
                        })
                        
                # Check for unusual operation patterns
                ops_in_window = []
                window_start = user_df.iloc[0]['timestamp_secu']
                
                for _, txn in user_df.iterrows():
                    if txn['timestamp_secu'] - window_start > time_window:
                        if len(ops_in_window) > 5:  # More than 5 ops in window
                            anomalies.append({
                                'transaction_id': txn['transaction_id'],
                                'anomaly_type': 'HIGH_FREQUENCY',
                                'user_id': user_id,
                                'operations_count': len(ops_in_window),
                                'detection_method': 'SEQUENCE'
                            })
                        ops_in_window = []
                        window_start = txn['timestamp_secu']
                    ops_in_window.append(txn['operation'])
                    
            return pd.DataFrame(anomalies)
            
        except Exception as e:
            logger.error(f"Error detecting sequence anomalies: {str(e)}")
            raise
            
    def detect_all_anomalies(
        self,
        df: pd.DataFrame,
        latency_cols: List[str],
        pattern_features: List[str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Run all anomaly detection methods.
        
        Args:
            df (pd.DataFrame): Input dataframe
            latency_cols (List[str]): Columns for latency analysis
            pattern_features (List[str]): Features for pattern analysis
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of anomaly results by type
        """
        try:
            results = {
                'latency_anomalies': self.detect_latency_anomalies(df, latency_cols),
                'pattern_anomalies': self.detect_pattern_anomalies(df, pattern_features),
                'sequence_anomalies': self.detect_sequence_anomalies(df)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {str(e)}")
            raise 