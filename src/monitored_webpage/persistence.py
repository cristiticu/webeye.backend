from boto3.dynamodb.conditions import Key
from monitored_webpage.exceptions import MonitoredWebpageNotFound
from monitored_webpage.model import MonitoredWebpage
import settings
from shared.dynamodb import dynamodb_table


class MonitoredWebpagePersistence():
    def __init__(self):
        self.webpages = dynamodb_table(settings.MONITORED_WEBPAGES_TABLE_NAME)

    def persist(self, payload: MonitoredWebpage):
        self.webpages.put_item(Item=payload.to_db_item())

    def get_all(self, u_guid: str):
        response = self.webpages.query(
            KeyConditionExpression=Key("u_guid").eq(u_guid))
        items = response.get("Items")

        return [MonitoredWebpage.from_db_item(item) for item in items]

    def get(self, u_guid: str, url: str):
        response = self.webpages.get_item(
            Key={"u_guid": u_guid, "url": url})
        item = response.get("Item")

        if item is None:
            raise MonitoredWebpageNotFound()

        return MonitoredWebpage.from_db_item(item)
