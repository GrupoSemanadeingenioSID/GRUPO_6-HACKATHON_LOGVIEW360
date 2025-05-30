"""
FastAPI application for the LogView360 analysis module.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import os
import pandas as pd
import numpy as np

from data_ingestion.merger import LogMerger
from processing.normalizer import LogNormalizer
from processing.latency_analysis import LatencyAnalyzer
from processing.flow_mapper import FlowMapper
from utils.logger import setup_logger
from utils.config import API_HOST, API_PORT, SOURCE_DIR

# Set up logger with file
log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'api.log')
logger = setup_logger('api', log_file=log_file)

# Create FastAPI app
app = FastAPI(
    title="LogView360 API",
    description="API for log analysis and transaction tracking",
    version="1.0.0"
)

# Initialize analyzers
merger = LogMerger(
    secucheck_path=f"{SOURCE_DIR}/logs_SecuCheck.json",
    midflow_path=f"{SOURCE_DIR}/logs_MidFlow_ESB.csv",
    corebank_path=f"{SOURCE_DIR}/logs_CoreBank.log"
)
normalizer = LogNormalizer()
latency_analyzer = LatencyAnalyzer()
flow_mapper = FlowMapper()

# Cache for analyzed data
analyzed_data = None
last_analysis_time = None
CACHE_DURATION_SECONDS = 300  # 5 minutes

class TransactionQuery(BaseModel):
    transaction_id: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class AnalysisResponse(BaseModel):
    timestamp: str
    latency_stats: Dict
    flow_stats: Dict
    anomaly_counts: Dict

async def refresh_analysis():
    """Background task to refresh analysis data."""
    global analyzed_data, last_analysis_time
    
    try:
        # Merge and analyze logs
        df = merger.merge_logs()
        df = normalizer.normalize_dataframe(df)
        
        # Calculate statistics
        latency_stats = latency_analyzer.calculate_basic_stats(
            df, ['service_latency', 'total_latency', 'e2e_latency']
        )
        
        # Analyze flows
        flow_patterns, flow_stats = flow_mapper.analyze_flow_patterns(df)
        flow_anomalies = flow_mapper.detect_anomalies(df)
        
        # Count anomalies by type
        pattern_anomalies = len(flow_anomalies[flow_anomalies['anomaly_types'].apply(
            lambda x: any('INCOMPLETE_FLOW' in t or 'MISSING_STAGES' in t for t in x)
        )])
        sequence_anomalies = len(flow_anomalies[flow_anomalies['anomaly_types'].apply(
            lambda x: 'LONG_DURATION' in x
        )])
        
        # Store results
        analyzed_data = {
            'df': df,
            'latency_stats': latency_stats,
            'flow_stats': flow_stats,
            'anomaly_counts': {
                'pattern': pattern_anomalies,
                'sequence': sequence_anomalies,
                'bottlenecks': len(latency_analyzer.find_bottlenecks(df))
            }
        }
        last_analysis_time = datetime.now()
        
    except Exception as e:
        logger.error(f"Error refreshing analysis: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint returning API status."""
    return {"status": "running", "service": "LogView360 API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "last_analysis": last_analysis_time.isoformat() if last_analysis_time else None
    }

@app.get("/transaction/{transaction_id}/trace")
async def get_transaction_trace(transaction_id: str):
    """
    Get the complete trace of a transaction across all systems.
    
    Args:
        transaction_id (str): ID of the transaction to trace
    """
    try:
        if not analyzed_data:
            await refresh_analysis()
            
        df = analyzed_data['df']
        transaction = df[df['transaction_id'] == transaction_id]
        
        if transaction.empty:
            raise HTTPException(status_code=404, detail="Transaction not found")
            
        flow, timestamps = flow_mapper.map_transaction_flow(df, transaction_id)
        
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
        
        return {
            "transaction_id": transaction_id,
            "flow_path": "->".join(flow) if flow else "",
            "timestamps": valid_timestamps,
            "latencies": latencies,
            "status": status,
            "amount": amount
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing transaction trace: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/latency")
async def get_latency_metrics(background_tasks: BackgroundTasks):
    """
    Get system-wide latency metrics.
    """
    try:
        # Check if we need to refresh the analysis
        if (not analyzed_data or 
            (datetime.now() - last_analysis_time).total_seconds() > CACHE_DURATION_SECONDS):
            background_tasks.add_task(refresh_analysis)
            
        if not analyzed_data:
            await refresh_analysis()
            
        return AnalysisResponse(
            timestamp=last_analysis_time.isoformat(),
            latency_stats=analyzed_data['latency_stats'],
            flow_stats=analyzed_data['flow_stats'],
            anomaly_counts=analyzed_data['anomaly_counts']
        )
    except Exception as e:
        logger.error(f"Error getting latency metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analysis/refresh")
async def force_refresh(background_tasks: BackgroundTasks):
    """
    Force a refresh of the analysis data.
    """
    try:
        background_tasks.add_task(refresh_analysis)
        return {"status": "refresh scheduled"}
    except Exception as e:
        logger.error(f"Error scheduling refresh: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    ) 