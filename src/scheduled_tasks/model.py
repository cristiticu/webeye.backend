from datetime import datetime
from typing import Generic, Literal, Mapping, TypeVar
from pydantic import UUID4, BaseModel

ConfigurationType = TypeVar("ConfigurationType", bound=BaseModel)


class ScheduledTask(BaseModel, Generic[ConfigurationType]):
    guid: UUID4
    u_guid: UUID4
    task_type: str
    interval: str
    days: str
    configuration: ConfigurationType
    c_at: datetime


class CheckConfiguration(BaseModel):
    url: str
    zones: list[Literal["america", "europe", "asia_pacific"]]
    check_string: str | None = None
    fail_on_status: list[int]
    timeout: int
    save_screenshot: bool


class ScheduledCheck(ScheduledTask[CheckConfiguration]):
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

        configuration = CheckConfiguration.model_validate(
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


class AggregationConfiguration(BaseModel):
    url: str


class ScheduledAggregation(ScheduledTask[AggregationConfiguration]):
    def to_db_item(self):
        h_key = str(self.u_guid)
        s_key = f"AGGREGATE#{self.configuration.url}#{self.guid}"
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

        configuration = AggregationConfiguration.model_validate(
            item["configuration"])

        item_payload = {
            **item,
            "interval": split_schedule[0],
            "days": split_schedule[1],
            "task_type": "AGGREGATE",
            "u_guid": u_guid,
            "guid": split_s_key[2],
            "configuration": configuration
        }
        return ScheduledAggregation.model_validate(item_payload)


class CreateScheduledCheck(BaseModel):
    url: str
    interval: Literal["1m", "2m", "5m", "10m", "15m", "30m"]
    days: Literal["all", "weekend", "weekdays"]
    zones: list[Literal["america", "europe", "asia_pacific"]]
    check_string: str | None = None
    fail_on_status: list[int] = [404, 500]
    timeout: int = 20000
