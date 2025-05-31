"""
Repository for handling user data operations.
"""
from datetime import datetime
from typing import Optional
import pandas as pd
from ..models.user import UserTransactions, Transaction
from .log_repository import LogRepository

class UserRepository:
    def __init__(self):
        self.log_repository = LogRepository()

    async def get_user_transactions(self, user_id: str) -> Optional[UserTransactions]:
        """
        Retrieve a user and their transactions by user_id.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            UserTransactions object if user exists, None otherwise
        """
        # Get all log data
        df = self.log_repository.get_data()
        
        # Filter logs for this user
        user_transactions = df[df['user_id'] == user_id]
        
        if user_transactions.empty:
            return None
            
        # Convert each transaction row to a Transaction model
        transactions = []
        for _, row in user_transactions.iterrows():
            transactions.append(
                Transaction(
                    transaction_id=row['transaction_id'],
                    ip_address=row['ip_address'],
                    timestamp=row['timestamp_core'] or row['timestamp_secu'],  # Use core timestamp or fallback to security
                    status=row['status'] == 'Completada',
                    operation=row['operation'],
                    account_type=row['account_type'],
                    amount=float(row['amount'])
                )
            )
        
        return UserTransactions(
            user_id=user_id,
            transactions=transactions
        ) 