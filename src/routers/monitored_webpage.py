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


@router.get("/{webpage_guid}")
def get_monitored_webpage(webpage_guid: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    raise MonitoredWebpageNotFound("NOT IMPLEMENTED")
    webpage = application_context.monitored_webpages.get(
        token.user_guid, webpage_guid)
    return webpage


@router.post("")
def create_monitored_webpage(webpage_payload: CreateMonitoredWebpage, token: Annotated[UserTokenData, Depends(user_token_data)]):
    webpage = application_context.monitored_webpages.create(
        token.user_guid, webpage_payload)
    return webpage
