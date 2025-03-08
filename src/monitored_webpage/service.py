from monitored_webpage.exceptions import MonitoredWebpageBusinessError, MonitoredWebpageNotFound
from monitored_webpage.model import CreateMonitoredWebpage
from monitored_webpage.persistence import MonitoredWebpagePersistence


class MonitoredWebpageService():
    def __init__(self, persistence: MonitoredWebpagePersistence):
        self._webpages = persistence

    async def get_all(self):
        return await self._webpages.get_all()

    async def get(self, id: str):
        webpage = await self._webpages.get_one(id)

        if webpage is None:
            raise MonitoredWebpageNotFound()

        return webpage

    async def create(self, payload: CreateMonitoredWebpage):
        webpage = await self._webpages.insert_monitored_webpage(payload)

        if webpage is None:
            raise MonitoredWebpageBusinessError(msg="Could not add webpage")

        return webpage
