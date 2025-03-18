import boto3
import boto3.dynamodb
import boto3.dynamodb.conditions
import settings
from shared.dynamodb import dynamodb_table
from user_account.exceptions import UserAccountNotFound
from user_account.model import UserAccount


class UserAccountPersistence():
    def __init__(self):
        self.users = dynamodb_table(settings.USER_ACCOUNTS_TABLE_NAME)

    def persist(self, payload: UserAccount):
        self.users.put_item(Item=payload.model_dump(mode="json"))

    def get_all(self):
        response = self.users.scan()
        items = response.get("Items")

        return [UserAccount.model_validate(item) for item in items]

    def get(self, guid: str):
        response = self.users.get_item(Key={"guid": guid})
        item = response.get("Item")

        if item is None:
            raise UserAccountNotFound()

        return UserAccount.model_validate(item)

    def get_by_email(self, email: str):
        response = self.users.query(KeyConditionExpression=boto3.dynamodb.conditions.Key(
            "email").eq(email), IndexName=settings.USER_ACCOUNTS_EMAIL_GSI)
        items = response.get("Items")

        if len(items) == 0:
            raise UserAccountNotFound()

        return UserAccount.model_validate(items[0])

    def delete(self, guid: str):
        self.users.delete_item(Key={"guid": guid})
