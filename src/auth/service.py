from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from pydantic import UUID4
from auth.model import LoggedInDevice
from auth.persistence import AuthPersistence
from auth.utils import create_access_token
from exceptions import CredentialsException
import settings
from user_account.exceptions import UserAccountNotFound
from passlib.context import CryptContext

from user_account.persistence import UserAccountPersistence

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class AuthService():
    def __init__(self, users_persistence: UserAccountPersistence, auth_persistence: AuthPersistence):
        self._users = users_persistence
        self._devices = auth_persistence

    def create_tokens(self, user_guid: UUID4, device_name: str | None = None):
        device_guid = uuid4()

        access_token = create_access_token({"user_guid": str(user_guid)})
        refresh_token = create_access_token(
            {
                "user_guid": str(user_guid),
                "device_guid": str(device_guid)
            }, 60 * 24)

        device = LoggedInDevice(
            guid=device_guid,
            user_guid=user_guid,
            refresh_token=token_context.hash(refresh_token),
            device_name=device_name if device_name != None else "Unknown Device",
            ttl=int(
                (datetime.now() + timedelta(days=settings.AUTH_REFRESH_RETENTION_DAYS)).timestamp()),
            last_login_at=datetime.now(timezone.utc)
        )

        self._devices.persist(device)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def authenticate(self, email: str, password: str, device_name: str | None = None):
        try:
            user = self._users.get_by_email(email)
        except UserAccountNotFound:
            raise CredentialsException(msg="Invalid credentials")

        if not pwd_context.verify(password, user.password):
            raise CredentialsException(msg="Invalid credentials")

        return self.create_tokens(user.guid, device_name)

    def refresh(self, refresh_token: str, user_guid: str, device_guid: str):
        logged_in_device = self._devices.get(user_guid, device_guid)

        if not token_context.verify(refresh_token, logged_in_device.refresh_token):
            self._devices.delete_token(user_guid, device_guid)
            raise CredentialsException(msg="Invalid credentials")

        new_access_token = create_access_token({"user_guid": str(user_guid)})
        new_refresh_token = create_access_token({
            "user_guid": str(user_guid),
            "device_guid": str(device_guid)},
            60 * 24
        )

        patched_device = LoggedInDevice.model_validate({
            **logged_in_device.model_dump(),
            "refresh_token": token_context.hash(new_refresh_token),
            "last_login_at": datetime.now(timezone.utc)
        })

        self._devices.persist(patched_device)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    def change_password(self, user_guid: str, old_password: str, new_password: str, device_name: str | None = None):
        user = self._users.get(user_guid)

        if not pwd_context.verify(old_password, user.password):
            raise CredentialsException(msg="Invalid credentials")

        new_hash = pwd_context.hash(new_password)
        user.password = new_hash

        self._users.persist(user)

        self.logout_all_sessions(user_guid)

        return self.create_tokens(UUID(user_guid), device_name)

    def get_logged_in_sessions(self, user_guid: str):
        return self._devices.get_all(user_guid)

    def logout(self, user_guid: str, device_guid: str):
        self._devices.delete_token(user_guid, device_guid)

    def logout_all_sessions(self, user_guid: str):
        self._devices.batch_delete_tokens(user_guid)
