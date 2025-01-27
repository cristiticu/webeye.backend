from fastapi import APIRouter
from user_account.persistence import UserAccountPersistence
from user_account.service import UserAccountService

router = APIRouter(prefix="/user", tags=["user"])

uap = UserAccountPersistence()
service = UserAccountService(uap)


@router.get("")
async def list_users():
    users = await service.get_all()
    return users


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await service.get(user_id)
    return user
