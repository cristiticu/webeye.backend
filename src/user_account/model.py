
from datetime import datetime

from pydantic import BaseModel
from shared.entity import Entity


class UserAccount(Entity):
    email: str
    password: str
    first_name: str
    last_name: str | None = None
    added_at: datetime


class AddUserAccount(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str | None = None
