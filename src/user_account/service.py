
from datetime import datetime, timezone
from uuid import uuid4
from user_account.exceptions import EmailAlreadyExists, UserAccountNotFound
from user_account.model import CreateUserAccount, UserAccount, UserAccountPatch
from user_account.persistence import UserAccountPersistence
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAccountService():
    def __init__(self, persistence: UserAccountPersistence):
        self._users = persistence

    def get_all(self):
        accounts = self._users.get_all()
        return [account.to_partial_account() for account in accounts]

    def get(self, id: str):
        account = self._users.get(id)
        return account.to_partial_account()

    def create(self, payload: CreateUserAccount):
        try:
            self._users.get_by_email(payload.email)
            raise EmailAlreadyExists()
        except UserAccountNotFound:
            pass

        account_payload = {
            **payload.model_dump(exclude_none=True),
            "guid": uuid4(),
            "password": pwd_context.hash(payload.password),
            "c_at": datetime.now(timezone.utc)
        }

        account = UserAccount.model_validate(account_payload)
        self._users.persist(account)

        return account.to_partial_account()

    def update(self, id: str, patch: UserAccountPatch):
        account = self._users.get(id)

        patched_account = UserAccount.model_validate(
            {
                **account.model_dump(),
                **patch.model_dump(exclude_none=True)
            })

        self._users.persist(patched_account)

        return patched_account.to_partial_account()

    def delete(self, id: str):
        self._users.delete(id)
