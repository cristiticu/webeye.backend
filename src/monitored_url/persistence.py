from exceptions import ItemBusinessError
from monitored_url.exceptions import MonitoredUrlBusinessError
from monitored_url.model import CreateMonitoredUrl, MonitoredUrl
from shared.database.db_repository import DbRepository


class MonitoredUrlPersistence(DbRepository[MonitoredUrl]):
    def __init__(self):
        super(MonitoredUrlPersistence, self).__init__(
            table_name="monitored_url", object_factory=lambda dict: MonitoredUrl(**dict))

    async def insert_monitored_url(self, url_payload: CreateMonitoredUrl):
        try:
            url = await self.insert(url_payload.model_dump())
            return url
        except ItemBusinessError as error:
            raise MonitoredUrlBusinessError(
                msg="URL exists already") from error

    async def update_monitored_url(self, patched_url: MonitoredUrl):
        try:
            url = await self.update(patched_url.model_dump())
            return url
        except ItemBusinessError as error:
            raise MonitoredUrlBusinessError(
                msg="URL exists already") from error
