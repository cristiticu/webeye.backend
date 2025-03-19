from boto3.dynamodb.conditions import Key
import settings
from shared.dynamodb import dynamodb_table
from user_account.exceptions import UserAccountNotFound
from user_account.model import UserAccount


class UserAccountPersistence():
    def __init__(self):
        self.users = dynamodb_table(settings.USER_ACCOUNTS_TABLE_NAME)

    def persist(self, payload: UserAccount):
        self.users.put_item(Item=payload.to_db_item())

    def get_all(self) -> list[UserAccount]:
        response = self.users.scan()
        items = response.get("Items")

        return [UserAccount.from_db_item(item) for item in items if str(item.get("s_key")).startswith("DATA")]

    def get(self, guid: str):
        response = self.users.get_item(Key={"guid": guid, "s_key": "DATA"})
        item = response.get("Item")

        if item is None:
            raise UserAccountNotFound()

        return UserAccount.from_db_item(item)

    def get_by_email(self, email: str):
        response = self.users.query(KeyConditionExpression=Key(
            "email").eq(email), IndexName=settings.USER_ACCOUNTS_EMAIL_GSI)
        items = response.get("Items")

        if len(items) == 0:
            raise UserAccountNotFound()

        return UserAccount.from_db_item(items[0])

    def delete(self, guid: str):
        self.users.delete_item(Key={"guid": guid})
