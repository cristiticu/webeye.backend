from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from user_account.model import CreateUserAccount, UserAccountPatch
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


@router.post("")
async def create_user(user_payload: CreateUserAccount):
    user = await service.create(user_payload)
    return user


@router.patch("{user_id}")
async def update_user(user_id: str, patch: UserAccountPatch):
    user = await service.update(user_id, patch)
    return user


@router.delete("{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    await service.delete(user_id)
