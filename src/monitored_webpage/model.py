from datetime import datetime
from pydantic import UUID4, BaseModel


class MonitoredWebpage(BaseModel):
    guid: UUID4
    user_guid: UUID4
    url: str
    added_at: datetime


class CreateMonitoredWebpage(BaseModel):
    url: str
