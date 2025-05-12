from typing import Annotated
from fastapi import APIRouter, Depends

from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from scheduled_tasks.model import CreateScheduledCheck, ScheduledCheckPatch


router = APIRouter(prefix="/task", tags=["scheduled task"])
application_context = ApplicationContext()


@router.get("/check")
def list_scheduled_checks(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    tasks = application_context.scheduled_tasks.get_all_checks(
        token.user_guid, url)
    return tasks


@router.post("/check")
def create_scheduled_check(check_payload: CreateScheduledCheck, token: Annotated[UserTokenData, Depends(user_token_data)]):
    task = application_context.scheduled_tasks.create_check(
        token.user_guid, check_payload)
    return task


@router.patch("/check/{guid}")
def update_scheduled_check(guid: str, patch: ScheduledCheckPatch, token: Annotated[UserTokenData, Depends(user_token_data)]):
    task = application_context.scheduled_tasks.update_check(
        token.user_guid, guid, patch
    )
    return task


@router.delete("/check")
def delete_scheduled_check(url: str, guid: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    application_context.scheduled_tasks.delete_scheduled_check(
        token.user_guid, url, guid)
