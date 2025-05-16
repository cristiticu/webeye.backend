from boto3.dynamodb.conditions import Key
from monitoring_events.exceptions import GeneralStatusNotFound, MonitoringEventNotFound
from monitoring_events.model import CurrentStatus, DowntimePeriod, GeneralContext, MonitoringEvent
from shared.dynamodb import dynamodb_table
import settings
from shared.utils import decode_last_evaluated_key, encode_last_evaluated_key


class MonitoringEventsPersistence():
    def __init__(self):
        self.events = dynamodb_table(
            settings.MONITORING_EVENTS_TABLE_NAME)

    def persist(self, payload: MonitoringEvent | CurrentStatus):
        self.events.put_item(Item=payload.to_db_item())

    def get_general_status(self, u_guid: str, url: str):
        h_key = f"{u_guid}#{url}"
        s_key = "GENERAL"

        response = self.events.get_item(Key={
            "h_key": h_key,
            "s_key": s_key
        })

        item = response.get("Item")

        if item is None:
            raise GeneralStatusNotFound()

        return GeneralContext.from_db_item(item)

    def get_regions_status(self, u_guid: str, url: str):
        h_key = f"{u_guid}#{url}"
        s_key = "CURRENT#"

        response = self.events.query(
            KeyConditionExpression=Key("h_key").eq(h_key) & Key("s_key").begins_with(s_key))

        items = response.get("Items")

        return [CurrentStatus.from_db_item(item) for item in items]

    def get_event(self, u_guid: str, url: str, c_at: str):
        h_key = f"{u_guid}#{url}"
        s_key = f"EVENT#{c_at}"

        response = self.events.get_item(Key={
            "h_key": h_key,
            "s_key": s_key
        })

        item = response.get("Item")

        if item is None:
            raise MonitoringEventNotFound()

        return MonitoringEvent.from_db_item(item)

    def get_events(self, u_guid: str, url: str, last_evaluated_key: str | None = None):
        h_key = f"{u_guid}#{url}"
        s_key = "EVENT#"

        kwargs = {
            "KeyConditionExpression": Key("h_key").eq(h_key) & Key("s_key").begins_with(s_key),
            "ScanIndexForward": False,
            "Limit": 25,
        }

        if last_evaluated_key:
            kwargs["ExclusiveStartKey"] = decode_last_evaluated_key(
                last_evaluated_key)

        response = self.events.query(
            **kwargs)

        items = response.get("Items")
        last_evaluated_key_response = response.get("LastEvaluatedKey")

        return {
            "data": [MonitoringEvent.from_db_item(item) for item in items],
            "meta": {
                "last_evaluated_key": encode_last_evaluated_key(last_evaluated_key_response) if last_evaluated_key_response else None
            }
        }

    def get_downtimes(self, u_guid: str, url: str, start_at: str, end_at: str):
        h_key = f"{u_guid}#{url}"
        s_key_start = f"DOWNTIME#{start_at}"
        s_key_end = f"DOWNTIME#{end_at}"

        response = self.events.query(KeyConditionExpression=Key("h_key").eq(
            h_key) & Key("s_key").between(s_key_start, s_key_end))

        items = response.get("Items")

        return [DowntimePeriod.from_db_item(item) for item in items]
