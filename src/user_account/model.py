
from datetime import datetime
from shared.entity import Entity


class UserAccount(Entity):
    email: str
    first_name: str
    last_name: str | None = None
    added_at: datetime
