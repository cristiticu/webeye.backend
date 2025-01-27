from shared.database.db_repository import DbRepository
from shared.database.exceptions import PsycopgGenericException
from user_account.model import UserAccount


class UserAccountPersistence(DbRepository[UserAccount]):
    def __init__(self):
        super(UserAccountPersistence, self).__init__(
            object_factory=lambda dict: UserAccount(**dict))

    async def get_user_accounts(self):
        async with self._cursor() as cursor:
            await cursor.execute("SELECT * FROM user_account_view_full")
            user_accounts = await cursor.fetchall()
            return user_accounts

    async def get_user_account(self, id: str):
        try:
            async with self._cursor() as cursor:
                await cursor.execute("SELECT * FROM user_account_view_full WHERE id=%s", (id,))
                user_account = await cursor.fetchone()
                return user_account
        except PsycopgGenericException as error:
            print("Encountered psycopg exception in User Persistence", error.message)
            return None
