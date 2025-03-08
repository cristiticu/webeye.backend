from fastapi import APIRouter

from context import ApplicationContext
from monitored_webpage.model import CreateMonitoredWebpage


router = APIRouter(prefix="/monitored-webpage", tags=["Monitored Webpage"])
application_context = ApplicationContext()


@router.get("")
async def list_webpages():
    webpages = await application_context.monitored_webpages.get_all()
    return webpages


@router.get("/{webpage_id}")
async def get_monitored_webpage(webpage_id: str):
    webpage = await application_context.monitored_webpages.get(webpage_id)
    return webpage


@router.post("")
async def create_monitored_webpage(webpage_payload: CreateMonitoredWebpage):
    webpage = await application_context.monitored_webpages.create(webpage_payload)
    return webpage
