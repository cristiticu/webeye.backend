from typing import Annotated
from fastapi import APIRouter, Depends, Query

from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext


router = APIRouter(prefix="/monitoring-event", tags=["monitoring event"])
application_context = ApplicationContext()


@router.get("")
def get_event(url: str, c_at: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.monitoring_events.get_event(token.user_guid, url, c_at)


@router.get("/list")
def list_events(url: str, token: Annotated[UserTokenData, Depends(user_token_data)], last_evaluated_key: str = Query(default=None)):
    return application_context.monitoring_events.get_events(token.user_guid, url, last_evaluated_key)


@router.get("/downtime")
def list_downtimes(url: str, start_at: str, end_at: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.monitoring_events.get_downtimes(token.user_guid, url, start_at, end_at)


@router.get("/status")
def get_general_status(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.monitoring_events.get_general_status(token.user_guid, url)


@router.get("/regions-status")
def get_regions_status(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    return application_context.monitoring_events.get_regions_status(token.user_guid, url)
