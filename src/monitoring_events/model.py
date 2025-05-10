from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel


class MonitoringEvent(BaseModel):
    u_guid: UUID4
    url: str
    region: str
    status: str
    results: Mapping | None = None
    error: str | None = None
    c_at: datetime
    ttl: int

    def to_db_item(self):
        h_key = f"{self.u_guid}#{self.url}"
        s_key = f"EVENT#{self.c_at.isoformat().replace("+00:00", "Z")}"

        return {
            "h_key": h_key,
            "s_key": s_key,
            "region": self.region,
            "status": self.status,
            "results": self.results,
            "error": self.error,
            "ttl": self.ttl,
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        split_h_key = item["h_key"].split("#")
        split_s_key = item["s_key"].split("#")

        item_payload = {
            **item,
            "u_guid": split_h_key[0],
            "url": split_h_key[1],
            "c_at": split_s_key[1]
        }

        return MonitoringEvent.model_validate(item_payload)


class DowntimePeriod(BaseModel):
    u_guid: UUID4
    url: str
    error: str | None = None
    s_at: datetime
    r_at: datetime

    def to_db_item(self):
        h_key = f"{self.u_guid}#{self.url}"
        s_key = f"DOWNTIME#{self.s_at.isoformat().replace("+00:00", "Z")}"

        return {
            "h_key": h_key,
            "s_key": s_key,
            "error": self.error,
            "r_at": self.r_at.isoformat().replace("+00:00", "Z")
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        split_h_key = item["h_key"].split("#")
        split_s_key = item["s_key"].split("#")

        item_payload = {
            **item,
            "u_guid": split_h_key[0],
            "url": split_h_key[1],
            "s_at": split_s_key[1]
        }

        return DowntimePeriod.model_validate(item_payload)


class CurrentStatus(BaseModel):
    u_guid: UUID4
    url: str
    region: str
    status: str
    error: str | None = None
    m_at: datetime | None = None

    def to_db_item(self):
        h_key = f"{self.u_guid}#{self.url}"
        s_key = f"CURRENT#{self.region}"

        return {
            "h_key": h_key,
            "s_key": s_key,
            "status": self.status,
            "error": self.error,
            "m_at": self.m_at.isoformat().replace("+00:00", "Z") if self.m_at else None,
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        split_h_key = item["h_key"].split("#")
        split_s_key = item["s_key"].split("#")

        item_payload = {
            **item,
            "u_guid": split_h_key[0],
            "url": split_h_key[1],
            "region": split_s_key[1]
        }

        return CurrentStatus.model_validate(item_payload)


class GeneralContext(BaseModel):
    u_guid: UUID4
    url: str
    status: str
    error: str | None = None
    downtime_s_at: datetime | None = None

    def to_db_item(self):
        h_key = f"{self.u_guid}#{self.url}"
        s_key = "GENERAL"

        return {
            "h_key": h_key,
            "s_key": s_key,
            "status": self.status,
            "error": self.error,
            "downtime_s_at": self.downtime_s_at.isoformat().replace("+00:00", "Z") if self.downtime_s_at else None,
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        split_h_key = item["h_key"].split("#")

        item_payload = {
            **item,
            "u_guid": split_h_key[0],
            "url": split_h_key[1],
        }

        return GeneralContext.model_validate(item_payload)
