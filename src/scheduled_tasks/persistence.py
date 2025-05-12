from contextlib import contextmanager
from scheduled_tasks.exceptions import ScheduledTaskNotFound
from scheduled_tasks.model import ScheduledAggregation, ScheduledCheck, ScheduledTask
import settings
from boto3.dynamodb.conditions import Key
from shared.dynamodb import dynamodb_table


class BatchWriter():
    def __init__(self, tasks):
        self.tasks = tasks
        self._batch_writer: AbstractContextManager = None  # type: ignore

    def __enter__(self):
        self._batch_writer = self.tasks.batch_writer()
        self._batch_writer.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._batch_writer.__exit__(exc_type, exc_val, exc_tb)

    def delete(self, u_guid: str, url: str, guid: str, type: str):
        h_key = u_guid
        s_key = f"{type}#{url}#{guid}"

        self._batch_writer.delete_item(Key={
            "h_key": h_key,
            "s_key": s_key
        })  # type: ignore


class ScheduledTasksPersistence():
    def __init__(self):
        self.tasks = dynamodb_table(settings.SCHEDULED_TASKS_TABLE_NAME)

    @contextmanager
    def batch_writer(self):
        with BatchWriter(self.tasks) as writer:
            yield writer

    def persist(self, payload: ScheduledCheck | ScheduledAggregation):
        self.tasks.put_item(Item=payload.to_db_item())

    def get_all_scheduled_checks(self, u_guid: str, url: str):
        h_key = u_guid
        s_key = f"CHECK#{url}#"

        response = self.tasks.query(
            KeyConditionExpression=Key("h_key").eq(h_key) &
            Key("s_key").begins_with(s_key)
        )
        items = response.get("Items")

        return [ScheduledCheck.from_db_item(item) for item in items]

    def get_scheduled_task(self, u_guid: str, url: str, guid: str, type: str):
        h_key = u_guid
        s_key = f"{type}#{url}#{guid}"

        response = self.tasks.get_item(
            Key={"h_key": h_key, "s_key": s_key})
        item = response.get("Item")

        if item is None:
            raise ScheduledTaskNotFound()

        return ScheduledTask.from_db_item(item)

    def delete_scheduled_tasks(self, u_guid: str, type: str, url: str):
        h_key = u_guid
        s_key = f"{type}#{url}#"

        response = self.tasks.query(KeyConditionExpression=Key(
            "h_key").eq(h_key) & Key("s_key").begins_with(s_key))

        items = response.get("Items")

        if len(items) > 0:
            with self.tasks.batch_writer() as batch:
                for item in items:
                    batch.delete_item(Key={
                        "h_key": item.get("h_key"),
                        "s_key": item.get("s_key")
                    })
