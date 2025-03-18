from auth.utils import create_access_token
from exceptions import CredentialsException
from user_account.exceptions import UserAccountNotFound
from user_account.persistence import UserAccountPersistence
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService():
    def __init__(self, users_persistence: UserAccountPersistence):
        self._users = users_persistence

    def authenticate(self, email: str, password: str):
        try:
            user = self._users.get_by_email(email)
        except UserAccountNotFound:
            raise CredentialsException(msg="Invalid credentials")

        if not pwd_context.verify(password, user.password):
            raise CredentialsException(msg="Invalid credentials")

        return create_access_token({"user_guid": str(user.guid)})
