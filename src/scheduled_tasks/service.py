from datetime import datetime, timezone
from uuid import uuid4
from monitored_webpage.service import MonitoredWebpageService
from scheduled_tasks.exceptions import ScheduledCheckAlreadyExists
from scheduled_tasks.model import AggregationConfiguration, CreateScheduledCheck, ScheduledAggregation, ScheduledCheck, CheckConfiguration, ScheduledCheckPatch

from scheduled_tasks.persistence import ScheduledTasksPersistence


class ScheduledTasksService():
    def __init__(self, tasks_persistence: ScheduledTasksPersistence, webpages: MonitoredWebpageService):
        self._tasks = tasks_persistence
        self._webpages = webpages

    def get_all_checks(self, u_guid: str, url: str):
        return self._tasks.get_all_scheduled_checks(u_guid, url)

    def create_check(self, u_guid: str, payload: CreateScheduledCheck):
        webpage = self._webpages.get(u_guid, payload.url)

        already_scheduled_checks = self._tasks.get_all_scheduled_checks(
            u_guid, payload.url)

        if len(already_scheduled_checks) != 0:
            raise ScheduledCheckAlreadyExists()

        check_configuration = CheckConfiguration(
            url=payload.url,
            zones=payload.zones,
            check_string=payload.check_string,
            accepted_status=payload.accepted_status,
            timeout=payload.timeout,
            save_screenshot=True
        )

        guid = uuid4()

        check_task_payload = {
            **payload.model_dump(),
            "guid": guid,
            "u_guid": u_guid,
            "w_guid": str(webpage.guid),
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
            "guid": guid,
            "u_guid": u_guid,
            "w_guid": str(webpage.guid),
            "task_type": "AGGREGATE",
            "c_at": datetime.now(timezone.utc),
            "configuration": aggregate_configuration
        }

        aggregate_task = ScheduledAggregation.model_validate(
            aggregate_task_payload)
        self._tasks.persist(aggregate_task)

        return check_task

    def update_check(self, u_guid: str, guid: str, patch: ScheduledCheckPatch):
        scheduled_check: ScheduledCheck = self._tasks.get_scheduled_task(
            u_guid, patch.url, guid, 'CHECK')
        scheduled_aggregation: ScheduledAggregation = self._tasks.get_scheduled_task(
            u_guid, patch.url, guid,  'AGGREGATE')

        patched_scheduled_check = ScheduledCheck.model_validate(
            {
                **scheduled_check.model_dump(),
                "configuration": {
                    **scheduled_check.configuration.model_dump(),
                    **patch.model_dump(exclude_none=True),
                    "check_string": patch.check_string
                },
                **patch.model_dump(exclude_none=True)
            }
        )

        patched_scheduled_aggregation = ScheduledAggregation.model_validate(
            {
                **scheduled_aggregation.model_dump(),
                **patch.model_dump(exclude_none=True)
            }
        )

        self._tasks.persist(patched_scheduled_check)
        self._tasks.persist(patched_scheduled_aggregation)

        return patched_scheduled_check

    def delete_scheduled_check(self, u_guid: str, url: str, guid: str):
        with self._tasks.batch_writer() as batch:
            batch.delete(u_guid, url, guid, 'CHECK')
            batch.delete(u_guid, url, guid, 'AGGREGATE')

    def delete_all_tasks(self, u_guid: str, url: str):
        self._tasks.delete_scheduled_tasks(u_guid, "CHECK", url)
        self._tasks.delete_scheduled_tasks(u_guid, "AGGREGATE", url)
