from fastapi import APIRouter, status, BackgroundTasks
from context import ApplicationContext
from user_account.model import CreateUserAccount, UserAccountPatch

router = APIRouter(prefix="/user", tags=["user account"])
application_context = ApplicationContext()


@router.get("")
def list_users():
    users = application_context.user_accounts.get_all()
    return users


@router.get("/{guid}")
def get_user(guid: str):
    user = application_context.user_accounts.get(guid)
    return user


@router.post("")
def create_user(user_payload: CreateUserAccount):
    user = application_context.user_accounts.create(user_payload)
    return user


@router.patch("/{guid}")
def update_user(guid: str, patch: UserAccountPatch):
    user = application_context.user_accounts.update(guid, patch)
    return user


@router.delete("/{guid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(guid: str, background_tasks: BackgroundTasks):
    webpages = application_context.monitored_webpages.get_all(guid)

    for webpage in webpages:
        background_tasks.add_task(
            application_context.monitored_webpages.delete, guid, webpage.url)
        background_tasks.add_task(
            application_context.scheduled_tasks.delete_all_tasks, guid, webpage.url)

    background_tasks.add_task(application_context.user_accounts.delete, guid)
