from datetime import datetime, timezone
from uuid import uuid4
from monitored_webpage.service import MonitoredWebpageService
from scheduled_tasks.exceptions import ScheduledCheckAlreadyExists
from scheduled_tasks.model import AggregationConfiguration, CreateScheduledCheck, ScheduledAggregation, ScheduledCheck, CheckConfiguration
from scheduled_tasks.persistence import ScheduledTasksPersistence


class ScheduledTasksService():
    def __init__(self, tasks_persistence: ScheduledTasksPersistence, webpages: MonitoredWebpageService):
        self._tasks = tasks_persistence
        self._webpages = webpages

    def get_all_checks(self, u_guid: str, url: str):
        return self._tasks.get_all_scheduled_checks(u_guid, url)

    def create_check(self, u_guid: str, payload: CreateScheduledCheck):
        self._webpages.get(u_guid, payload.url)

        already_scheduled_checks = self._tasks.get_all_scheduled_checks(
            u_guid, payload.url)

        if len(already_scheduled_checks) != 0:
            raise ScheduledCheckAlreadyExists()

        check_configuration = CheckConfiguration(
            url=payload.url, zones=payload.zones)

        check_task_payload = {
            **payload.model_dump(),
            "guid": uuid4(),
            "u_guid": u_guid,
            "task_type": "CHECK",
            "c_at": datetime.now(timezone.utc),
            "configuration": check_configuration
        }

        check_task = ScheduledCheck.model_validate(check_task_payload)
        self._tasks.persist(check_task)

        aggregate_configuration = AggregationConfiguration(
            url=payload.url
        )

        aggregate_task_payload = {
            **payload.model_dump(),
            "guid": uuid4(),
            "u_guid": u_guid,
            "task_type": "AGGREGATE",
            "c_at": datetime.now(timezone.utc),
            "configuration": aggregate_configuration
        }

        aggregate_task = ScheduledAggregation.model_validate(
            aggregate_task_payload)
        self._tasks.persist(aggregate_task)

        return check_task
