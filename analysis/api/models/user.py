from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class Transaction(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    ip_address: str = Field(..., description="IP address where the transaction was made")
    timestamp: datetime = Field(..., description="When the transaction occurred")
    status: bool = Field(..., description="True if transaction was successful, False otherwise")
    operation: str = Field(..., description="Type of operation (transferir, consignar, retirar)")
    account_type: str = Field(..., description="Type of account (ahorros, corriente)")
    amount: float = Field(..., description="Amount of the transaction")

class UserTransactions(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    transactions: List[Transaction] = Field(default_factory=list, description="List of user transactions") 