from datetime import datetime
from pydantic import UUID4, BaseModel, ConfigDict


class UserAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    email: str
    password: str
    first_name: str
    last_name: str | None = None
    added_at: datetime


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
