from pydantic import BaseModel


class UserTokenData(BaseModel, frozen=True):
    raw_token: str
    user_guid: str
