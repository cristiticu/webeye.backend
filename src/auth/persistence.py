from auth.exceptions import LoggedInDeviceNotFound
from auth.model import LoggedInDevice
import settings
from boto3.dynamodb.conditions import Key
from shared.dynamodb import dynamodb_table


class AuthPersistence():
    def __init__(self):
        self.users = dynamodb_table(settings.USER_ACCOUNTS_TABLE_NAME)

    def persist(self, payload: LoggedInDevice):
        self.users.put_item(Item=payload.to_db_item())

    def get(self, user_guid: str, guid: str):
        response = self.users.get_item(
            Key={"guid": user_guid, "s_key": f"TOKEN#{guid}"})
        item = response.get("Item")

        if item is None:
            raise LoggedInDeviceNotFound()

        return LoggedInDevice.from_db_item(item)

    def get_all(self, user_guid: str):
        response = self.users.query(KeyConditionExpression=Key(
            'guid').eq(user_guid) & Key('s_key').begins_with('TOKEN'))

        items = response.get("Items")

        return [LoggedInDevice.from_db_item(item) for item in items]

    def delete(self, user_guid: str, guid: str):
        self.users.delete_item(
            Key={"guid": user_guid, "s_key": f"TOKEN#{guid}"})
