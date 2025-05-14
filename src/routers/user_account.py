from typing import Annotated
from fastapi import APIRouter, Depends, status, BackgroundTasks
from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from user_account.model import CreateUserAccount, UserAccountPatch

router = APIRouter(prefix="/user", tags=["user account"])
application_context = ApplicationContext()


@router.post("")
def create_user(user_payload: CreateUserAccount):
    user = application_context.user_accounts.create(user_payload)
    return user


@router.get("")
def get_user(token: Annotated[UserTokenData, Depends(user_token_data)]):
    user = application_context.user_accounts.get(token.user_guid)
    return user


@router.patch("")
def update_user(patch: UserAccountPatch, token: Annotated[UserTokenData, Depends(user_token_data)]):
    user = application_context.user_accounts.update(token.user_guid, patch)
    return user


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(background_tasks: BackgroundTasks, token: Annotated[UserTokenData, Depends(user_token_data)]):
    webpages = application_context.monitored_webpages.get_all(token.user_guid)

    for webpage in webpages:
        background_tasks.add_task(
            application_context.monitored_webpages.delete, token.user_guid, webpage.url)
        background_tasks.add_task(
            application_context.scheduled_tasks.delete_all_tasks, token.user_guid, webpage.url)

    background_tasks.add_task(
        application_context.user_accounts.delete, token.user_guid)
