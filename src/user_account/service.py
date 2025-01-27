
from user_account.exceptions import UserAccountNotFound
from user_account.persistence import UserAccountPersistence


class UserAccountService():
    def __init__(self, persistence: UserAccountPersistence):
        self._users = persistence

    async def get_all(self):
        accounts = await self._users.get_user_accounts()
        return accounts

    async def get(self, id: str):
        account = await self._users.get_user_account(id)

        if account is None:
            raise UserAccountNotFound()

        return account
