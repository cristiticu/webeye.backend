from datetime import datetime
from uuid import UUID, uuid4
from user_account.exceptions import UserBusinessError
from user_account.model import CreateUserAccount, UserAccount


class MockedUserAccountPersistence():
    def __init__(self, *args, **kwargs):
        self._users: list[UserAccount] = []

    async def get_all(self):
        return self._users

    async def get_one(self, user_id: str):
        user = [
            user for user in self._users if user.id == UUID(user_id)]

        if len(user) == 1:
            return user[0]
        else:
            return None

    async def insert_user_account(self, user_payload: CreateUserAccount):
        for user in self._users:
            if user.email == user_payload.email:
                raise UserBusinessError()

        account = UserAccount(
            **{**user_payload.model_dump(), "added_at": datetime.now(), "id": uuid4()})
        self._users.append(account)

        return account
