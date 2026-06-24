from fastapi import APIRouter,status,HTTPException,Depends
from service.jwt_token import get_current_user
from service.database_operations import delete_user_data, fetch_user

router = APIRouter(prefix="/api")

@router.delete("/user_delete", tags=["User"])
def delete_user(user=Depends(get_current_user)):
    try:
        current_user = fetch_user(user["id"])
        delete_user_data(current_user.id)
        return {"message": "User deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))