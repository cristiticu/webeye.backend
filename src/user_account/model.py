from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel, ConfigDict


class UserAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    email: str
    password: str
    first_name: str
    last_name: str | None = None
    added_at: datetime

    def to_db_item(self):
        return {
            **self.model_dump(mode="json"),
            "s_key": 'DATA'
        }

    def to_partial_account(self):
        return PartialUserAccount.model_validate(self, from_attributes=True)

    @classmethod
    def from_db_item(cls, item: Mapping):
        return UserAccount.model_validate(item)


class PartialUserAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    email: str
    first_name: str
    last_name: str | None = None
    added_at: datetime


class CreateUserAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    email: str
    password: str
    first_name: str
    last_name: str | None = None


class UserAccountPatch(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
