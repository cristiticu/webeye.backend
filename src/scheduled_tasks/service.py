from datetime import datetime, timezone
from uuid import uuid4
from monitored_webpage.service import MonitoredWebpageService
from scheduled_tasks.model import CreateScheduledCheck, ScheduledCheck, ScheduledCheckConfiguration
from scheduled_tasks.persistence import ScheduledTasksPersistence


class ScheduledTasksService():
    def __init__(self, tasks_persistence: ScheduledTasksPersistence, webpages: MonitoredWebpageService):
        self._tasks = tasks_persistence
        self._webpages = webpages

    def get_all_checks(self, u_guid: str, url: str):
        return self._tasks.get_all_scheduled_checks(u_guid, url)

    def create_check(self, u_guid: str, payload: CreateScheduledCheck):
        self._webpages.get(u_guid, payload.url)

        configuration = ScheduledCheckConfiguration(
            url=payload.url, regions=payload.regions)

        task_payload = {
            **payload.model_dump(),
            "guid": uuid4(),
            "u_guid": u_guid,
            "task_type": "CHECK",
            "c_at": datetime.now(timezone.utc),
            "configuration": configuration
        }

        task = ScheduledCheck.model_validate(task_payload)
        self._tasks.persist(task)

        return task
