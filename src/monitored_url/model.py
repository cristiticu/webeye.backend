from datetime import datetime

from pydantic import BaseModel
from shared.entity import Entity


class MonitoredUrl(Entity):
    user_account_id: str
    url: str
    added_at: datetime


class CreateMonitoredUrl(BaseModel):
    user_account_id: str
    url: str
