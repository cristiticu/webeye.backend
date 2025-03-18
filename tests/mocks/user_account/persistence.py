from uuid import UUID
from user_account.exceptions import UserAccountNotFound
from user_account.model import UserAccount


class MockedUserAccountPersistence():
    def __init__(self, *args, **kwargs):
        self._users: list[UserAccount] = []

    def get_all(self):
        return self._users

    def get(self, user_id: str):
        user = [
            user for user in self._users if user.guid == UUID(user_id)]

        if len(user) == 1:
            return user[0]
        else:
            raise UserAccountNotFound()

    def get_by_email(self, email: str):
        user = [
            user for user in self._users if user.email == email]

        if len(user) == 1:
            return user[0]
        else:
            raise UserAccountNotFound()

    def persist(self, payload: UserAccount):
        self._users.append(payload)
