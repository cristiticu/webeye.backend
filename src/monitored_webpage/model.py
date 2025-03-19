from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel


class MonitoredWebpage(BaseModel):
    guid: UUID4
    user_guid: UUID4
    url: str
    added_at: datetime

    def to_db_item(self):
        return self.model_dump(mode='json')

    @classmethod
    def from_db_item(cls, item: Mapping):
        return MonitoredWebpage.model_validate(item)


class CreateMonitoredWebpage(BaseModel):
    url: str
