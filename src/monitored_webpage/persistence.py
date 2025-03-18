import boto3
import boto3.dynamodb
import boto3.dynamodb.conditions
from monitored_webpage.exceptions import MonitoredWebpageNotFound
from monitored_webpage.model import MonitoredWebpage
import settings
from shared.dynamodb import dynamodb_table


class MonitoredWebpagePersistence():
    def __init__(self):
        self.webpages = dynamodb_table(settings.MONITORED_WEBPAGES_TABLE_NAME)

    def persist(self, payload: MonitoredWebpage):
        self.webpages.put_item(Item=payload.model_dump(mode="json"))

    def get_all(self, user_guid: str):
        response = self.webpages.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_guid").eq(user_guid))
        items = response.get("Items")

        return [MonitoredWebpage.model_validate(item) for item in items]

    def get(self, user_guid: str, url: str):
        response = self.webpages.get_item(
            Key={"user_guid": user_guid, "url": url})
        item = response.get("Item")

        if item is None:
            raise MonitoredWebpageNotFound()

        return MonitoredWebpage.model_validate(item)
