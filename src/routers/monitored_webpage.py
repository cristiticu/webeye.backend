from fastapi import APIRouter

from monitored_webpage.model import CreateMonitoredWebpage
from monitored_webpage.persistence import MonitoredWebpagePersistence
from monitored_webpage.service import MonitoredWebpageService


router = APIRouter(prefix="/monitored-webpage", tags=["Monitored Webpage"])

mup = MonitoredWebpagePersistence()
service = MonitoredWebpageService(mup)


@router.get("")
async def list_webpages():
    webpages = await service.get_all()
    return webpages


@router.get("/{webpage_id}")
async def get_monitored_webpage(webpage_id: str):
    webpage = await service.get(webpage_id)
    return webpage


@router.post("")
async def create_monitored_webpage(webpage_payload: CreateMonitoredWebpage):
    webpage = await service.create(webpage_payload)
    return webpage
