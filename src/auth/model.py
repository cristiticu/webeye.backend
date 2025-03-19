from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel


class UserTokenData(BaseModel, frozen=True):
    raw_token: str
    user_guid: str


class RefreshTokenData(BaseModel, frozen=True):
    raw_token: str
    user_guid: str
    device_guid: str


class LoggedInDevice(BaseModel):
    guid: UUID4
    user_guid: UUID4
    refresh_token: str
    device_name: str
    last_login_at: datetime

    def to_db_item(self):
        return {
            "guid": str(self.user_guid),
            "s_key": f"TOKEN#{self.guid}",
            "refresh_token": self.refresh_token,
            "device_name": self.device_name,
            "last_login_at": self.last_login_at.isoformat().replace("+00:00", "Z")
        }

    @classmethod
    def from_db_item(cls, item: Mapping):
        split_s_key = item["s_key"].split("#")
        item_payload = {
            **item,
            "guid": split_s_key[1],
            "user_guid": item["guid"],
        }
        return LoggedInDevice.model_validate(item_payload)
