"""
Service layer for log analysis operations.
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta, timezone
import pandas as pd
import numpy as np

from ..repositories.log_repository import LogRepository
from ..models.schemas import (
    TransactionTrace, 
    AnalysisResponse, 
    BottleneckDetail,
    BottleneckSummary,
    TimeRangeQuery,
    LatencyTrend,
    PaginationParams
)
from utils.logger import setup_logger

logger = setup_logger('service')

class LogService:
    def __init__(self, repository: LogRepository):
        """Initialize service with repository."""
        self.repository = repository
        
    def needs_refresh(self) -> bool:
        """Check if data needs refresh."""
        last_update = self.repository.get_last_update()
        if last_update is None:
            return True
        return (datetime.now() - last_update).total_seconds() > 300
        
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

    def get_bottlenecks(self, query: TimeRangeQuery) -> List[BottleneckDetail]:
        """
        Get detailed bottleneck information within a time range.
        
        Args:
            query: Time range and filtering parameters
            
        Returns:
            List of bottleneck details
        """
        df = self.repository.get_data()
        
        # Apply time range filter if provided
        if query.start_time:
            df = df[df['timestamp_secu'] >= query.start_time]
        if query.end_time:
            df = df[df['timestamp_secu'] <= query.end_time]
            
        # Apply module and operation filters if provided
        if query.module:
            df = df[df['module'] == query.module]
        if query.operation:
            df = df[df['operation'] == query.operation]
            
        # Get bottlenecks using analyzer
        bottlenecks_df = self.repository.latency_analyzer.find_bottlenecks(df)
        
        # Convert to list of BottleneckDetail
        bottlenecks = []
        for _, row in bottlenecks_df.iterrows():
            bottlenecks.append(
                BottleneckDetail(
                    transaction_id=row['transaction_id'],
                    stage=row['stage'],
                    latency=row['latency'],
                    threshold=row['threshold'],
                    operation=row['operation'],
                    module=row['module']
                )
            )
            
        # Apply limit
        return bottlenecks[:query.limit]
        
    def get_bottlenecks_summary(
        self,
        start_time: Optional[datetime],
        end_time: Optional[datetime]
    ) -> BottleneckSummary:
        """
        Get summary statistics about bottlenecks.
        
        Args:
            start_time: Optional start of time range
            end_time: Optional end of time range
            
        Returns:
            Summary statistics
        """
        df = self.repository.get_data()
        
        # Apply time range filter if provided
        if start_time:
            df = df[df['timestamp_secu'] >= start_time]
        if end_time:
            df = df[df['timestamp_secu'] <= end_time]
            
        # Get bottlenecks
        bottlenecks_df = self.repository.latency_analyzer.find_bottlenecks(df)
        
        if bottlenecks_df.empty:
            return BottleneckSummary(
                total_bottlenecks=0,
                by_stage={},
                by_operation={},
                by_module={},
                avg_latency={},
                threshold_exceeded={}
            )
            
        # Calculate summary statistics
        by_stage = bottlenecks_df['stage'].value_counts().to_dict()
        by_operation = bottlenecks_df['operation'].value_counts().to_dict()
        by_module = bottlenecks_df['module'].value_counts().to_dict()
        
        # Calculate average latencies by stage
        avg_latency = bottlenecks_df.groupby('stage')['latency'].mean().to_dict()
        
        # Calculate average threshold exceedance
        bottlenecks_df['exceeded_by'] = bottlenecks_df['latency'] - bottlenecks_df['threshold']
        threshold_exceeded = bottlenecks_df.groupby('stage')['exceeded_by'].mean().to_dict()
        
        return BottleneckSummary(
            total_bottlenecks=len(bottlenecks_df),
            by_stage=by_stage,
            by_operation=by_operation,
            by_module=by_module,
            avg_latency=avg_latency,
            threshold_exceeded=threshold_exceeded
        )
        
    def get_latency_trends(
        self,
        start_time: datetime,
        end_time: datetime,
        window: str
    ) -> List[LatencyTrend]:
        """
        Get latency trends over time.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            window: Time window for aggregation
            
        Returns:
            List of latency trends by time window
        """
        df = self.repository.get_data()
        
        # Filter by time range
        df = df[
            (df['timestamp_secu'] >= start_time) &
            (df['timestamp_secu'] <= end_time)
        ]
        
        if df.empty:
            return []
            
        # Resample by time window
        df.set_index('timestamp_secu', inplace=True)
        resampled = df.resample(window)
        
        trends = []
        for name, group in resampled:
            if not group.empty:
                # Calculate metrics for this window
                bottlenecks = self.repository.latency_analyzer.find_bottlenecks(group)
                
                trends.append(
                    LatencyTrend(
                        timestamp=name,
                        avg_latency=group['e2e_latency'].mean(),
                        percentile_95=group['e2e_latency'].quantile(0.95),
                        percentile_99=group['e2e_latency'].quantile(0.99),
                        num_bottlenecks=len(bottlenecks)
                    )
                )
                
        return trends 

    def get_merged_data(self, pagination: PaginationParams) -> Dict:
        """
        Get all merged data from the three log sources with complete traceability.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            Dict: Dictionary containing paginated merged data with complete transaction flow
        """
        try:
            logger.info("Getting data from repository...")
            # Get the merged and normalized data
            df = self.repository.get_data()
            logger.info(f"Got dataframe with shape: {df.shape}")
            
            # Calculate pagination
            total_records = len(df)
            total_pages = (total_records + pagination.page_size - 1) // pagination.page_size
            
            # Validate page number
            if pagination.page > total_pages and total_pages > 0:
                pagination.page = total_pages
            
            # Calculate slice indices
            start_idx = (pagination.page - 1) * pagination.page_size
            end_idx = min(start_idx + pagination.page_size, total_records)
            
            # Slice dataframe
            df_page = df.iloc[start_idx:end_idx]
            
            # Convert to format más simple y estandarizado
            records = []
            for _, row in df_page.iterrows():
                try:
                    record = {
                        'transaction_id': str(row['transaction_id']),
                        'timestamps': {
                            'security': row['timestamp_secu'].replace(tzinfo=timezone.utc).isoformat() if pd.notna(row['timestamp_secu']) else None,
                            'middleware_start': row['start_time'].replace(tzinfo=timezone.utc).isoformat() if pd.notna(row['start_time']) else None,
                            'middleware_end': row['end_time'].replace(tzinfo=timezone.utc).isoformat() if pd.notna(row['end_time']) else None,
                            'core_banking': row['timestamp_core'].replace(tzinfo=timezone.utc).isoformat() if pd.notna(row['timestamp_core']) else None
                        },
                        'operation': str(row['operation']) if pd.notna(row['operation']) else None,
                        'status': str(row['status']) if pd.notna(row['status']) else None,
                        'amount': float(row['amount']) if pd.notna(row['amount']) else None,
                        'validation': {
                            'result': str(row['validation_result']) if pd.notna(row['validation_result']) else None,
                            'failure_reason': str(row['failure_reason']) if pd.notna(row['failure_reason']) else None,
                            'verifications': str(row['verifications']).split(',') if pd.notna(row['verifications']) else []
                        },
                        'latencies': {
                            'service': float(row['service_latency']) if pd.notna(row['service_latency']) else None,
                            'total': float(row['total_latency']) if pd.notna(row['total_latency']) else None,
                            'end_to_end': float(row['e2e_latency']) if pd.notna(row['e2e_latency']) else None
                        },
                        'user_info': {
                            'user_id': str(row['user_id']) if pd.notna(row['user_id']) else None,
                            'ip_address': str(row['ip_address']) if pd.notna(row['ip_address']) else None
                        },
                        'system_info': {
                            'module': str(row['module']) if pd.notna(row['module']) else None,
                            'account_type': str(row['account_type']) if pd.notna(row['account_type']) else None
                        },
                        'flow_status': {
                            'has_security_check': bool(row['has_security_check']) if pd.notna(row['has_security_check']) else False,
                            'has_middleware_flow': bool(row['has_middleware_flow']) if pd.notna(row['has_middleware_flow']) else False,
                            'has_core_banking': bool(row['has_core_banking']) if pd.notna(row['has_core_banking']) else False,
                            'completion_percentage': float(row['completion_pct']) if pd.notna(row['completion_pct']) else 0.0
                        }
                    }
                    records.append(record)
                except Exception as e:
                    logger.error(f"Error processing row: {str(e)}")
                    logger.error(f"Row data: {row.to_dict()}")
                    continue
            
            logger.info(f"Successfully processed {len(records)} records for page {pagination.page}")
            
            # Create pagination metadata
            metadata = {
                'total_records': total_records,
                'total_pages': total_pages,
                'current_page': pagination.page,
                'page_size': pagination.page_size,
                'has_next': pagination.page < total_pages,
                'has_previous': pagination.page > 1
            }
            
            result = {
                'metadata': metadata,
                'data': records
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting merged data: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise 