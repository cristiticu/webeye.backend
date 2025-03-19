from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel


class ScheduledTask(BaseModel):
    guid: UUID4
    user_guid: UUID4
    task_type: str
    url: str
    interval: str
    days: str
    region: str
    added_at: datetime

    def to_db_item(self):
        return {
            "h_key": f"{self.user_guid}#{self.url}",
            "task_key": f"{self.task_type}#{self.guid}",
            "schedule": f"{self.interval}#{self.days}",
            "region": self.region,
            "added_at": self.added_at.isoformat().replace("+00:00", "Z")
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        split_h_key = item["h_key"].split("#")
        split_task_key = item["task_key"].split("#")
        split_schedule = item["schedule"].split("#")

        item_payload = {
            **item,
            "interval": split_schedule[0],
            "days": split_schedule[1],
            "user_guid": split_h_key[0],
            "url": split_h_key[1],
            "task_type": split_task_key[0],
            "guid": split_task_key[1],
        }
        return ScheduledTask.model_validate(item_payload)


class CreateScheduledTask(BaseModel):
    url: str
    task_type: str
    interval: str
    days: str
    region: str
