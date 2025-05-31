"""
Service for handling user-related operations.
"""
from typing import Optional
from ..models.user import UserTransactions
from ..repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def get_user_transactions(self, user_id: str) -> Optional[UserTransactions]:
        """
        Get a user and their transactions.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            UserTransactions object if user exists, None otherwise
        """
        return await self.repository.get_user_transactions(user_id) 