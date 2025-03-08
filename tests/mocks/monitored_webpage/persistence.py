from uuid import UUID
from monitored_webpage.model import MonitoredWebpage


class MockedMonitoredWebpagePersistence():
    def __init__(self, *args, **kwargs):
        self._webpages: list[MonitoredWebpage] = []

    async def get_all(self):
        return self._webpages

    async def get_one(self, webpage_id: str):
        webpage = [
            webpage for webpage in self._webpages if webpage.id == UUID(webpage_id)]

        if len(webpage) == 1:
            return webpage[0]
        else:
            return None
