"""
Flow mapper for tracking transaction paths through the system.
"""
from typing import Dict, List, Optional, Tuple
import pandas as pd
import networkx as nx
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger('flow_mapper')

class FlowMapper:
    """Mapper for transaction flows through the system."""
    
    def __init__(self):
        """Initialize the flow mapper."""
        # Define expected flow stages
        self.stages = [
            'SECURITY_CHECK',
            'MIDDLEWARE_REQUEST',
            'MIDDLEWARE_RESPONSE',
            'CORE_BANKING'
        ]
        
    def create_flow_graph(self) -> nx.DiGraph:
        """
        Create a directed graph representing the expected flow.
        
        Returns:
            nx.DiGraph: Graph of expected transaction flow
        """
        G = nx.DiGraph()
        
        # Add nodes for each stage
        for stage in self.stages:
            G.add_node(stage)
            
        # Add edges representing valid transitions
        G.add_edge('SECURITY_CHECK', 'MIDDLEWARE_REQUEST')
        G.add_edge('MIDDLEWARE_REQUEST', 'MIDDLEWARE_RESPONSE')
        G.add_edge('MIDDLEWARE_RESPONSE', 'CORE_BANKING')
        
        return G
        
    def map_transaction_flow(
        self,
        df: pd.DataFrame,
        transaction_id: str
    ) -> Tuple[List[str], List[float]]:
        """
        Map the flow of a specific transaction.
        
        Args:
            df (pd.DataFrame): Input dataframe with merged logs
            transaction_id (str): Transaction ID to map
            
        Returns:
            Tuple[List[str], List[float]]: List of stages and their timestamps
        """
        try:
            # Get transaction data
            txn_df = df[df['transaction_id'] == transaction_id]
            if txn_df.empty:
                logger.warning(f"No data found for transaction {transaction_id}")
                return [], []
                
            txn = txn_df.iloc[0]
            
            flow = []
            timestamps = []
            
            # Check security stage
            if pd.notna(txn.get('timestamp_secu')):
                flow.append('SECURITY_CHECK')
                timestamps.append(txn['timestamp_secu'].timestamp())
                
            # Check middleware stages
            has_middleware = (
                pd.notna(txn.get('service_latency')) and
                pd.notna(txn.get('start_time')) and
                pd.notna(txn.get('end_time'))
            )
            
            if has_middleware:
                # Add middleware stages in sequence
                flow.extend(['MIDDLEWARE_REQUEST', 'MIDDLEWARE_RESPONSE'])
                timestamps.extend([
                    txn['start_time'].timestamp(),
                    txn['end_time'].timestamp()
                ])
                
            # Check core banking stage
            if pd.notna(txn.get('timestamp_core')):
                flow.append('CORE_BANKING')
                timestamps.append(txn['timestamp_core'].timestamp())
                
            return flow, timestamps
            
        except Exception as e:
            logger.error(f"Error mapping transaction flow: {str(e)}")
            raise
            
    def analyze_flow_patterns(
        self,
        df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, Dict[str, float]]:
        """
        Analyze flow patterns across all transactions.
        
        Args:
            df (pd.DataFrame): Input dataframe with merged logs
            
        Returns:
            Tuple[pd.DataFrame, Dict[str, float]]:
                DataFrame with flow patterns and
                Dictionary with pattern statistics
        """
        try:
            patterns = []
            flow_counts = {}
            
            # Analyze each transaction
            for _, txn in df.iterrows():
                flow, timestamps = self.map_transaction_flow(df, txn['transaction_id'])
                flow_path = '->'.join(flow)
                
                # Count unique flow patterns
                flow_counts[flow_path] = flow_counts.get(flow_path, 0) + 1
                
                pattern = {
                    'transaction_id': txn['transaction_id'],
                    'flow_path': flow_path,
                    'num_stages': len(flow),
                    'is_complete': len(flow) == len(self.stages),
                    'total_duration': max(timestamps) - min(timestamps) if timestamps else 0,
                    'start_time': min(timestamps) if timestamps else None,
                    'end_time': max(timestamps) if timestamps else None
                }
                
                patterns.append(pattern)
                
            # Log flow pattern distribution
            logger.info("Flow pattern distribution:")
            for pattern, count in flow_counts.items():
                logger.info(f"  {pattern}: {count} transactions")
                
            # Create patterns dataframe
            patterns_df = pd.DataFrame(patterns)
            
            # Calculate statistics
            stats = {
                'complete_flow_pct': (patterns_df['is_complete'].mean() * 100),
                'avg_stages': patterns_df['num_stages'].mean(),
                'avg_duration': patterns_df['total_duration'].mean(),
                'min_duration': patterns_df['total_duration'].min(),
                'max_duration': patterns_df['total_duration'].max()
            }
            
            return patterns_df, stats
            
        except Exception as e:
            logger.error(f"Error analyzing flow patterns: {str(e)}")
            raise
            
    def detect_anomalies(
        self,
        df: pd.DataFrame,
        duration_threshold: float = 15.0,  # Ajustado basado en e2e_latency
        min_stages: int = 2  # Mínimo número de etapas esperadas
    ) -> pd.DataFrame:
        """
        Detect anomalies in transaction flows.
        
        Args:
            df (pd.DataFrame): Input dataframe with merged logs
            duration_threshold (float): Threshold for duration anomalies in seconds
            min_stages (int): Minimum number of stages expected in a valid flow
            
        Returns:
            pd.DataFrame: DataFrame with detected anomalies
        """
        try:
            patterns_df, stats = self.analyze_flow_patterns(df)
            
            # Calculate dynamic threshold based on e2e_latency stats if available
            if 'e2e_latency' in df.columns:
                mean_e2e = df['e2e_latency'].mean()
                std_e2e = df['e2e_latency'].std()
                if not pd.isna(mean_e2e) and not pd.isna(std_e2e):
                    duration_threshold = mean_e2e + (2 * std_e2e)  # 2 desviaciones estándar
                    logger.info(f"Dynamic duration threshold: {duration_threshold:.2f}s")
            
            # Detect various types of anomalies
            anomalies = []
            
            for _, pattern in patterns_df.iterrows():
                anomaly_types = []
                details = []
                
                # Check for incomplete flows
                if not pattern['is_complete']:
                    anomaly_types.append('INCOMPLETE_FLOW')
                    details.append(f"Missing stages: {len(self.stages) - pattern['num_stages']}")
                
                # Check for minimum stages
                if pattern['num_stages'] < min_stages:
                    anomaly_types.append('MISSING_STAGES')
                    details.append(f"Only {pattern['num_stages']} stages found")
                
                # Check for long duration
                if pattern['total_duration'] > duration_threshold:
                    anomaly_types.append('LONG_DURATION')
                    details.append(f"Duration: {pattern['total_duration']:.2f}s")
                    
                if anomaly_types:
                    anomalies.append({
                        'transaction_id': pattern['transaction_id'],
                        'flow_path': pattern['flow_path'],
                        'anomaly_types': anomaly_types,
                        'details': details,
                        'total_duration': pattern['total_duration'],
                        'num_stages': pattern['num_stages']
                    })
            
            # Create anomalies dataframe
            anomalies_df = pd.DataFrame(anomalies)
            
            # Log anomaly statistics
            if not anomalies_df.empty:
                logger.info(f"Found {len(anomalies_df)} anomalies")
                for anomaly_type in ['INCOMPLETE_FLOW', 'MISSING_STAGES', 'LONG_DURATION']:
                    count = len(anomalies_df[anomalies_df['anomaly_types'].apply(lambda x: anomaly_type in x)])
                    logger.info(f"  {anomaly_type}: {count}")
            else:
                logger.info("No anomalies detected")
                    
            return anomalies_df if not anomalies_df.empty else pd.DataFrame({
                'transaction_id': [],
                'flow_path': [],
                'anomaly_types': [],
                'details': [],
                'total_duration': [],
                'num_stages': []
            })
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            raise 