from fastapi import APIRouter

from monitored_url.model import CreateMonitoredUrl
from monitored_url.persistence import MonitoredUrlPersistence
from monitored_url.service import MonitoredUrlService


router = APIRouter(prefix="/monitored-url", tags=["Monitored URL"])

mup = MonitoredUrlPersistence()
service = MonitoredUrlService(mup)


@router.get("")
async def list_urls():
    urls = await service.get_all()
    return urls


@router.get("/{url_id}")
async def get_monitored_url(url_id: str):
    url = await service.get(url_id)
    return url


@router.post("")
async def create_monitored_url(url_payload: CreateMonitoredUrl):
    url = await service.create(url_payload)
    return url
