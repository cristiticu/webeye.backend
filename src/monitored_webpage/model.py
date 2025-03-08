from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from shared.entity import Entity


class MonitoredWebpage(Entity):
    user_account_id: UUID
    url: str
    added_at: datetime


class CreateMonitoredWebpage(BaseModel):
    user_account_id: str
    url: str
