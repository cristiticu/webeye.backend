
from user_account.exceptions import UserAccountNotFound, UserCreateError
from user_account.model import CreateUserAccount, PartialUserAccount, UserAccount, UserAccountPatch
from user_account.persistence import UserAccountPersistence
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAccountService():
    def __init__(self, persistence: UserAccountPersistence):
        self._users = persistence

    async def get_all(self):
        accounts = await self._users.get_user_accounts()

        return [PartialUserAccount(**{**account.model_dump()}) for account in accounts]

    async def get(self, id: str):
        account = await self._users.get_user_account(id)

        if account is None:
            raise UserAccountNotFound()

        return PartialUserAccount(**{**account.model_dump()})

    async def create(self, payload: CreateUserAccount):
        account = await self._users.insert_user_account(
            CreateUserAccount(
                **{**payload.model_dump(exclude_none=True),
                   "password": pwd_context.hash(payload.password)}
            ))

        if account is None:
            raise UserCreateError()

        return PartialUserAccount(**{**account.model_dump()})

    async def update(self, id: str, patch: UserAccountPatch):
        account = await self._users.get_user_account(id)

        if account is None:
            raise UserAccountNotFound()

        patch.password = pwd_context.hash(
            patch.password) if patch.password else None

        patched_account = UserAccount(
            **{**account.model_dump(), **patch.model_dump(exclude_none=True)})

        response = await self._users.update_user_account(patched_account)

        if response is None:
            raise UserCreateError("Could not update user!")

        return PartialUserAccount(**{**response.model_dump()})
