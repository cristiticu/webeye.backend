from datetime import datetime
from typing import Literal, Mapping
from pydantic import UUID4, BaseModel


class ScheduledTask(BaseModel):
    guid: UUID4
    u_guid: UUID4
    task_type: Literal["CHECK"]
    interval: str
    days: str
    c_at: datetime

    def to_db_item(self) -> dict[str, str]:
        h_key = str(self.u_guid)
        s_key = f"{self.task_type}#{self.guid}"
        schedule = f"{self.interval}#{self.days}"

        return {
            "h_key": h_key,
            "s_key": s_key,
            "schedule": schedule,
            "c_at": self.c_at.isoformat().replace("+00:00", "Z")
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        u_guid = item["h_key"]
        split_s_key = item["s_key"].split("#")
        split_schedule = item["schedule"].split("#")

        item_payload = {
            **item,
            "guid": split_s_key[len(split_s_key) - 1],
            "u_guid": u_guid,
            "task_type": split_s_key[0],
            "interval": split_schedule[0],
            "days": split_schedule[1],
        }
        return ScheduledTask.model_validate(item_payload)


class ScheduledCheckConfiguration(BaseModel):
    url: str
    regions: list[Literal["america", "europe", "asia_pacific"]]


class ScheduledCheck(ScheduledTask):
    configuration: ScheduledCheckConfiguration

    def to_db_item(self):
        h_key = str(self.u_guid)
        s_key = f"CHECK#{self.configuration.url}#{self.guid}"
        schedule = f"{self.interval}#{self.days}"

        return {
            "h_key": h_key,
            "s_key": s_key,
            "schedule": schedule,
            "configuration": self.configuration.model_dump(mode="json"),
            "c_at": self.c_at.isoformat().replace("+00:00", "Z")
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        u_guid = item["h_key"]
        split_s_key = item["s_key"].split("#")
        split_schedule = item["schedule"].split("#")

        configuration = ScheduledCheckConfiguration.model_validate(
            item["configuration"])

        item_payload = {
            **item,
            "interval": split_schedule[0],
            "days": split_schedule[1],
            "task_type": "CHECK",
            "u_guid": u_guid,
            "guid": split_s_key[2],
            "configuration": configuration
        }
        return ScheduledCheck.model_validate(item_payload)


class CreateScheduledCheck(BaseModel):
    url: str
    interval: Literal["30s", "1m", "2m", "5m", "10m", "15m", "30m"]
    days: Literal["all", "weekend", "weekdays"]
    regions: list[Literal["america", "europe", "asia_pacific"]]
