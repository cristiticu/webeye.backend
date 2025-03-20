from typing import Annotated
from fastapi import APIRouter, Depends

from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from scheduled_tasks.model import CreateScheduledTask


router = APIRouter(prefix="/task", tags=["scheduled task"])
application_context = ApplicationContext()


@router.get("")
def list_scheduled_tasks(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    tasks = application_context.scheduled_tasks.get_all(token.user_guid, url)
    return tasks


@router.post("")
def create_scheduled_task(task_payload: CreateScheduledTask, token: Annotated[UserTokenData, Depends(user_token_data)]):
    task = application_context.scheduled_tasks.create(
        token.user_guid, task_payload)
    return task
