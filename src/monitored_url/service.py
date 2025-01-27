from monitored_url.exceptions import MonitoredUrlBusinessError, MonitoredUrlNotFound
from monitored_url.model import CreateMonitoredUrl
from monitored_url.persistence import MonitoredUrlPersistence


class MonitoredUrlService():
    def __init__(self, persistence: MonitoredUrlPersistence):
        self._urls = persistence

    async def get_all(self):
        return await self._urls.get_all()

    async def get(self, id: str):
        url = await self._urls.get_one(id)

        if url is None:
            raise MonitoredUrlNotFound()

        return url

    async def create(self, payload: CreateMonitoredUrl):
        url = await self._urls.insert_monitored_url(payload)

        if url is None:
            raise MonitoredUrlBusinessError(msg="Could not create URL")

        return url
