from exceptions import ItemBusinessError
from shared.database.db_repository import DbRepository
from user_account.exceptions import UserBusinessError
from user_account.model import CreateUserAccount, UserAccount


class UserAccountPersistence(DbRepository[UserAccount]):
    def __init__(self):
        super(UserAccountPersistence, self).__init__(table_name="user_account",
                                                     object_factory=lambda dict: UserAccount(**dict))

    async def insert_user_account(self, user_payload: CreateUserAccount):
        try:
            user = await self.insert(user_payload.model_dump())
            return user
        except ItemBusinessError as error:
            raise UserBusinessError(
                msg="An user with the email address already exists!") from error

    async def update_user_account(self, patched_user: UserAccount):
        try:
            user = await self.update(patched_user.model_dump())
            return user
        except ItemBusinessError as error:
            raise UserBusinessError(
                msg="An user with the email address already exists!") from error
