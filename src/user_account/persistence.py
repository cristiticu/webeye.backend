from shared.database.db_repository import DbRepository
from shared.database.exceptions import PsycopgGenericException, PsycopgIntegrityException
from user_account.exceptions import UserCreateError
from user_account.model import CreateUserAccount, UserAccount


class UserAccountPersistence(DbRepository[UserAccount]):
    def __init__(self):
        super(UserAccountPersistence, self).__init__(
            object_factory=lambda dict: UserAccount(**dict))

    async def get_user_accounts(self) -> list[UserAccount]:
        try:
            async with self._cursor() as cursor:
                await cursor.execute("SELECT * FROM user_account_view")
                user_accounts = await cursor.fetchall()
                return user_accounts
        except PsycopgGenericException as error:
            print(
                "Encountered psycopg exception in get user accounts at User Persistence", error.message)
            return list[UserAccount]()

    async def get_user_account(self, id: str) -> UserAccount | None:
        try:
            async with self._cursor() as cursor:
                await cursor.execute("SELECT * FROM user_account_view WHERE id=%s", (id,))
                user_account = await cursor.fetchone()
                return user_account
        except PsycopgGenericException as error:
            print(
                "Encountered psycopg exception in get user account at User Persistence", error.message)
            return None

    async def insert_user_account(self, user_payload: CreateUserAccount) -> UserAccount | None:
        try:
            async with self._cursor() as cursor:
                await cursor.execute(

                    "INSERT INTO user_account_view(email, first_name, last_name, password)\
                            VALUES (%s, %s, %s, %s)\
                            RETURNING *",
                    (user_payload.email, user_payload.first_name,
                     user_payload.last_name, user_payload.password)
                )

                new_account = await cursor.fetchone()
                print(new_account)

                return new_account
        except PsycopgIntegrityException as error:
            raise UserCreateError(
                msg="An user with the email address already exists!") from error

        except PsycopgGenericException as error:
            print(
                "Encountered psycopg exception in insert user account at User Persistence", error.message)
            return None

    async def update_user_account(self, patched_user: UserAccount) -> UserAccount | None:
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    "UPDATE user_account_view\
                        SET email=%s, first_name=%s, last_name=%s, password=%s\
                        WHERE id=%s\
                        RETURNING *",
                    (patched_user.email, patched_user.first_name,
                     patched_user.last_name, patched_user.password, patched_user.id)
                )

                patched_account = await cursor.fetchone()

                return patched_account
        except PsycopgIntegrityException as error:
            raise UserCreateError(
                msg="Email address already in use!") from error
        except PsycopgGenericException as error:
            print(
                "Encountered psycopg exception in update user account at User Persistence", error.message)
            return None
