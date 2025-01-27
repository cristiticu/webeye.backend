
from datetime import datetime

from pydantic import BaseModel
from shared.entity import Entity


class UserAccount(Entity):
    email: str
    password: str
    first_name: str
    last_name: str | None = None
    added_at: datetime


class PartialUserAccount(Entity):
    email: str
    first_name: str
    last_name: str | None = None
    added_at: datetime


class CreateUserAccount(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str | None = None


class UserAccountPatch(BaseModel):
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
