from scheduled_tasks.exceptions import ScheduledTaskNotFound
from scheduled_tasks.model import ScheduledTask
import settings
from boto3.dynamodb.conditions import Key
from shared.dynamodb import dynamodb_table


class ScheduledTasksPersistence():
    def __init__(self):
        self.tasks = dynamodb_table(settings.SCHEDULED_TASKS_TABLE_NAME)

    def persist(self, payload: ScheduledTask):
        self.tasks.put_item(Item=payload.to_db_item())

    def get_all(self, user_guid: str, url: str):
        h_key = f"{user_guid}#{url}"

        response = self.tasks.query(
            KeyConditionExpression=Key("h_key").eq(h_key))
        items = response.get("Items")

        return [ScheduledTask.from_db_item(item) for item in items]

    def get(self, guid: str, user_guid: str, url: str, task_type: str):
        h_key = f"{user_guid}#{url}"
        task_key = f"{task_type}#{guid}"

        response = self.tasks.get_item(
            Key={"h_key": h_key, "task_key": task_key})
        item = response.get("Item")

        if item is None:
            raise ScheduledTaskNotFound()

        return ScheduledTask.from_db_item(item)
