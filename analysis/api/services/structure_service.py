"""
Service for handling data structure information.
"""
from typing import Dict, List
import pandas as pd
from datetime import datetime

from ..models.schemas import DataFieldInfo, DataStructureResponse
from ..repositories.log_repository import LogRepository
from utils.logger import setup_logger

logger = setup_logger('structure_service')

class StructureService:
    def __init__(self, repository: LogRepository):
        """Initialize service with repository."""
        self.repository = repository

    def get_data_structure(self) -> DataStructureResponse:
        """
        Get the complete data structure information.
        
        Returns:
            DataStructureResponse: Detailed information about data structure
        """
        try:
            # Get sample data
            df = self.repository.get_data()
            
            # Define field categories
            timestamp_fields = [
                DataFieldInfo(
                    name="timestamp_secu",
                    type="datetime",
                    description="Timestamp from security check",
                    nullable=True,
                    example="2025-05-13 08:00:10"
                ),
                DataFieldInfo(
                    name="start_time",
                    type="datetime",
                    description="Start time of middleware processing",
                    nullable=True,
                    example="2025-05-13 08:00:11"
                ),
                DataFieldInfo(
                    name="end_time",
                    type="datetime",
                    description="End time of middleware processing",
                    nullable=True,
                    example="2025-05-13 08:00:12"
                ),
                DataFieldInfo(
                    name="timestamp_core",
                    type="datetime",
                    description="Timestamp from core banking",
                    nullable=True,
                    example="2025-05-13 08:00:13"
                )
            ]
            
            transaction_fields = [
                DataFieldInfo(
                    name="transaction_id",
                    type="string",
                    description="Unique identifier for the transaction",
                    nullable=False,
                    example="txn-0000"
                ),
                DataFieldInfo(
                    name="operation",
                    type="string",
                    description="Type of operation (DEPOSIT, WITHDRAWAL, TRANSFER)",
                    nullable=False,
                    example="DEPOSIT"
                ),
                DataFieldInfo(
                    name="amount",
                    type="float",
                    description="Transaction amount",
                    nullable=True,
                    example="1000.00"
                ),
                DataFieldInfo(
                    name="account_type",
                    type="string",
                    description="Type of account (SAVINGS, CHECKING)",
                    nullable=True,
                    example="SAVINGS"
                )
            ]
            
            user_fields = [
                DataFieldInfo(
                    name="user_id",
                    type="string",
                    description="User identifier",
                    nullable=False,
                    example="user123"
                ),
                DataFieldInfo(
                    name="ip_address",
                    type="string",
                    description="IP address of the user",
                    nullable=False,
                    example="192.168.1.1"
                ),
                DataFieldInfo(
                    name="module",
                    type="string",
                    description="Module used (MOBILE, WEB, API)",
                    nullable=False,
                    example="MOBILE"
                )
            ]
            
            latency_fields = [
                DataFieldInfo(
                    name="service_latency",
                    type="float",
                    description="Service processing latency in seconds",
                    nullable=True,
                    example="0.236"
                ),
                DataFieldInfo(
                    name="total_latency",
                    type="float",
                    description="Total middleware latency in seconds",
                    nullable=True,
                    example="0.500"
                ),
                DataFieldInfo(
                    name="e2e_latency",
                    type="float",
                    description="End-to-end latency in seconds",
                    nullable=True,
                    example="1.200"
                )
            ]
            
            status_fields = [
                DataFieldInfo(
                    name="status",
                    type="string",
                    description="Transaction status (COMPLETED, FAILED, etc.)",
                    nullable=False,
                    example="COMPLETED"
                ),
                DataFieldInfo(
                    name="validation_result",
                    type="string",
                    description="Security validation result",
                    nullable=True,
                    example="APPROVED"
                ),
                DataFieldInfo(
                    name="failure_reason",
                    type="string",
                    description="Reason for failure if transaction failed",
                    nullable=True,
                    example="INSUFFICIENT_FUNDS"
                )
            ]
            
            metadata_fields = [
                DataFieldInfo(
                    name="verifications",
                    type="string",
                    description="List of security verifications performed",
                    nullable=True,
                    example="IP_CHECK,FRAUD_CHECK"
                ),
                DataFieldInfo(
                    name="has_security_check",
                    type="boolean",
                    description="Whether security check was performed",
                    nullable=False,
                    example="true"
                ),
                DataFieldInfo(
                    name="has_middleware_flow",
                    type="boolean",
                    description="Whether middleware processing occurred",
                    nullable=False,
                    example="true"
                ),
                DataFieldInfo(
                    name="has_core_banking",
                    type="boolean",
                    description="Whether core banking processing occurred",
                    nullable=False,
                    example="true"
                ),
                DataFieldInfo(
                    name="completion_pct",
                    type="float",
                    description="Percentage of flow completion",
                    nullable=False,
                    example="100.0"
                )
            ]
            
            return DataStructureResponse(
                total_fields=len(df.columns),
                timestamp_fields=timestamp_fields,
                transaction_fields=transaction_fields,
                user_fields=user_fields,
                latency_fields=latency_fields,
                status_fields=status_fields,
                metadata_fields=metadata_fields
            )
            
        except Exception as e:
            logger.error(f"Error getting data structure: {str(e)}")
            raise 