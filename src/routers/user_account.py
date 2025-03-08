from fastapi import APIRouter, status
from context import ApplicationContext
from user_account.model import CreateUserAccount, UserAccountPatch

router = APIRouter(prefix="/user", tags=["User Account"])
application_context = ApplicationContext()


@router.get("")
async def list_users():
    users = await application_context.user_accounts.get_all()
    return users


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await application_context.user_accounts.get(user_id)
    return user


@router.post("")
async def create_user(user_payload: CreateUserAccount):
    user = await application_context.user_accounts.create(user_payload)
    return user


@router.patch("{user_id}")
async def update_user(user_id: str, patch: UserAccountPatch):
    user = await application_context.user_accounts.update(user_id, patch)
    return user


@router.delete("{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    await application_context.user_accounts.delete(user_id)
