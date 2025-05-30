from fastapi import APIRouter, HTTPException
from api.services.user_service import UserService
from api.models.user import UserTransactions

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.get("/{user_id}/transactions", response_model=UserTransactions)
async def get_user_transactions(user_id: str) -> UserTransactions:
    """
    Get a user and their transactions by user ID.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        UserTransactions object containing user details and their transactions
        
    Raises:
        HTTPException: If user is not found
    """
    result = await service.get_user_transactions(user_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )
    return result 