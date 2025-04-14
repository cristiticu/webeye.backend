from typing import Annotated
from fastapi import APIRouter, Depends

from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from scheduled_tasks.model import CreateScheduledCheck


router = APIRouter(prefix="/task", tags=["scheduled task"])
application_context = ApplicationContext()


@router.get("")
def list_scheduled_checks(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    tasks = application_context.scheduled_tasks.get_all_checks(
        token.user_guid, url)
    return tasks


@router.post("")
def create_scheduled_check(check_payload: CreateScheduledCheck, token: Annotated[UserTokenData, Depends(user_token_data)]):
    task = application_context.scheduled_tasks.create_check(
        token.user_guid, check_payload)
    return task
