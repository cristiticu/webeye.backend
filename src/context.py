from auth.persistence import AuthPersistence
from auth.service import AuthService
from monitored_webpage.persistence import MonitoredWebpagePersistence
from monitored_webpage.service import MonitoredWebpageService
from monitoring_events.persistence import MonitoringEventsPersistence
from monitoring_events.service import MonitoringEventsService
from scheduled_tasks.persistence import ScheduledTasksPersistence
from scheduled_tasks.service import ScheduledTasksService
from user_account.persistence import UserAccountPersistence
from user_account.service import UserAccountService


class ApplicationContext():
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ApplicationContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._user_accounts_persistence = UserAccountPersistence()
        self.user_accounts = UserAccountService(
            self._user_accounts_persistence)

        self._authentication_persistence = AuthPersistence()
        self.authentication = AuthService(
            self._user_accounts_persistence, self._authentication_persistence)

        self._monitored_webpages_persistence = MonitoredWebpagePersistence()
        self.monitored_webpages = MonitoredWebpageService(
            self._monitored_webpages_persistence, self.user_accounts)

        self._scheduled_tasks_persistence = ScheduledTasksPersistence()
        self.scheduled_tasks = ScheduledTasksService(
            self._scheduled_tasks_persistence, self.monitored_webpages)

        self._monitoring_events_persistence = MonitoringEventsPersistence()
        self.monitoring_events = MonitoringEventsService(
            self._monitoring_events_persistence)
