from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel, ConfigDict


class UserAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    email: str
    password: str
    f_name: str
    l_name: str | None = None
    c_at: datetime

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
    f_name: str
    l_name: str | None = None
    c_at: datetime


class CreateUserAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    email: str
    password: str
    f_name: str
    l_name: str | None = None


class UserAccountPatch(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    email: str | None = None
    password: str | None = None
    f_name: str | None = None
    l_name: str | None = None
