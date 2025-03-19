from datetime import datetime, timezone
from uuid import uuid4
from monitored_webpage.exceptions import MonitoredWebpageNotFound
from monitored_webpage.service import MonitoredWebpageService
from scheduled_tasks.model import CreateScheduledTask, ScheduledTask
from scheduled_tasks.persistence import ScheduledTasksPersistence


class ScheduledTasksService():
    def __init__(self, tasks_persistence: ScheduledTasksPersistence, webpages: MonitoredWebpageService):
        self._tasks = tasks_persistence
        self._webpages = webpages

    def get_all(self, user_guid: str, url: str):
        return self._tasks.get_all(user_guid, url)

    def create(self, user_guid: str, payload: CreateScheduledTask):
        self._webpages.get(user_guid, payload.url)

        task_payload = {
            **payload.model_dump(),
            "guid": uuid4(),
            "user_guid": user_guid,
            "added_at": datetime.now(timezone.utc)
        }

        task = ScheduledTask.model_validate(task_payload)
        self._tasks.persist(task)

        return task
