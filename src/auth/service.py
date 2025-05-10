from datetime import datetime, timedelta, timezone
from uuid import uuid4
from auth.model import LoggedInDevice
from auth.persistence import AuthPersistence
from auth.utils import create_access_token
from exceptions import CredentialsException
from user_account.exceptions import UserAccountNotFound
from passlib.context import CryptContext

from user_account.persistence import UserAccountPersistence

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class AuthService():
    def __init__(self, users_persistence: UserAccountPersistence, auth_persistence: AuthPersistence):
        self._users = users_persistence
        self._devices = auth_persistence

    def authenticate(self, email: str, password: str, refresh_token_retention_days: int, device_name: str | None = None):
        try:
            user = self._users.get_by_email(email)
        except UserAccountNotFound:
            raise CredentialsException(msg="Invalid credentials")

        if not pwd_context.verify(password, user.password):
            raise CredentialsException(msg="Invalid credentials")

        device_guid = uuid4()

        access_token = create_access_token({"user_guid": str(user.guid)})
        refresh_token = create_access_token(
            {
                "user_guid": str(user.guid),
                "device_guid": str(device_guid)
            }, 60 * 24)

        device = LoggedInDevice(
            guid=device_guid,
            user_guid=user.guid,
            refresh_token=token_context.hash(refresh_token),
            device_name=device_name if device_name != None else "Unknown Device",
            ttl=int(
                (datetime.now() + timedelta(days=refresh_token_retention_days)).timestamp()),
            last_login_at=datetime.now(timezone.utc)
        )

        self._devices.persist(device)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def refresh(self, refresh_token: str, user_guid: str, device_guid: str):
        logged_in_device = self._devices.get(user_guid, device_guid)

        if not token_context.verify(refresh_token, logged_in_device.refresh_token):
            self._devices.delete(user_guid, device_guid)
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

    def get_logged_in_sessions(self, user_guid: str):
        return self._devices.get_all(user_guid)

    def logout(self, user_guid: str, device_guid: str):
        self._devices.delete(user_guid, device_guid)

    def logout_all_sessions(self, user_guid: str):
        self._devices.batch_delete(user_guid)
