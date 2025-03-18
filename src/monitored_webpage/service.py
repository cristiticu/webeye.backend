from datetime import datetime, timezone
from uuid import UUID, uuid4
import requests
from monitored_webpage.exceptions import MonitoredWebpageAlreadyExists, MonitoredWebpageNotFound, UrlNotReachable
from monitored_webpage.model import CreateMonitoredWebpage, MonitoredWebpage
from monitored_webpage.persistence import MonitoredWebpagePersistence
from user_account.exceptions import UserAccountNotFound
from user_account.service import UserAccountService


class MonitoredWebpageService():
    def __init__(self, persistence: MonitoredWebpagePersistence, users: UserAccountService):
        self._webpages = persistence
        self._users = users

    def is_url_reachable_or_raise(self, url: str):
        try:
            response = requests.head(url, timeout=10)
            return True
        except requests.exceptions.RequestException:
            raise UrlNotReachable()

    def get_all(self, user_guid: str):
        return self._webpages.get_all(user_guid)

    def get(self, user_guid: str, url: str):
        webpage = self._webpages.get(user_guid, url)
        return webpage

    def create(self, user_guid: str, payload: CreateMonitoredWebpage):
        self.is_url_reachable_or_raise(payload.url)
        self._users.get(user_guid)

        try:
            self._webpages.get(user_guid, payload.url)
            raise MonitoredWebpageAlreadyExists()
        except MonitoredWebpageNotFound:
            pass

        webpage_payload = {
            **payload.model_dump(),
            "user_guid": UUID(user_guid),
            "guid": uuid4(),
            "added_at": datetime.now(timezone.utc)
        }

        webpage = MonitoredWebpage.model_validate(
            webpage_payload)
        self._webpages.persist(webpage)

        return webpage
