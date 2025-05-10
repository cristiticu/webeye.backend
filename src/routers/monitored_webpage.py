from typing import Annotated
from fastapi import APIRouter, Depends
from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from monitored_webpage.exceptions import MonitoredWebpageNotFound
from monitored_webpage.model import CreateMonitoredWebpage


router = APIRouter(prefix="/monitored-webpage", tags=["monitored webpage"])
application_context = ApplicationContext()


@router.get("")
def list_webpages(token: Annotated[UserTokenData, Depends(user_token_data)]):
    webpages = application_context.monitored_webpages.get_all(token.user_guid)
    return webpages


@router.post("")
def create_monitored_webpage(webpage_payload: CreateMonitoredWebpage, token: Annotated[UserTokenData, Depends(user_token_data)]):
    webpage = application_context.monitored_webpages.create(
        token.user_guid, webpage_payload)
    return webpage


@router.delete("")
def delete_monitored_webpage(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    application_context.monitored_webpages.delete(token.user_guid, url)
    application_context.scheduled_tasks.delete_all_tasks(token.user_guid, url)
