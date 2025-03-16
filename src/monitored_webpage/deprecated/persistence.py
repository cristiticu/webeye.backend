from exceptions import ItemBusinessError
from monitored_webpage.exceptions import MonitoredWebpageBusinessError
from monitored_webpage.model import MonitoredWebpage, CreateMonitoredWebpage
from shared.psycopg.db_repository import DbRepository


class MonitoredWebpagePersistence(DbRepository[MonitoredWebpage]):
    def __init__(self):
        super(MonitoredWebpagePersistence, self).__init__(
            table_name="monitored_webpage", object_factory=lambda dict: MonitoredWebpage(**dict), is_view=True)

    async def insert_monitored_webpage(self, webpage_payload: CreateMonitoredWebpage):
        try:
            webpage = await self.insert(webpage_payload.model_dump())
            return webpage
        except ItemBusinessError as error:
            raise MonitoredWebpageBusinessError(
                msg="Webpage exists already") from error

    async def update_monitored_webpage(self, patched_webpage: MonitoredWebpage):
        try:
            webpage = await self.update(str(patched_webpage.id), patched_webpage.model_dump())
            return webpage
        except ItemBusinessError as error:
            raise MonitoredWebpageBusinessError(
                msg="Webpage exists already") from error
