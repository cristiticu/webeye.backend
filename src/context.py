from monitored_webpage.persistence import MonitoredWebpagePersistence
from monitored_webpage.service import MonitoredWebpageService
from user_account.persistence import UserAccountPersistence
from user_account.service import UserAccountService


class ApplicationContext():
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ApplicationContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._monitored_webpages_persistence = MonitoredWebpagePersistence()
        self.monitored_webpages = MonitoredWebpageService(
            self._monitored_webpages_persistence)

        self._user_accounts_persistence = UserAccountPersistence()
        self.user_accounts = UserAccountService(
            self._user_accounts_persistence)
