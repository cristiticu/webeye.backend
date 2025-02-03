from psycopg import Error
from exceptions import DatabaseException


class PsycopgGenericException(DatabaseException):
    def __init__(self, error: Error):
        super(PsycopgGenericException, self).__init__(
            msg=f'''{error.sqlstate}:
                hint: {error.diag.message_hint}
                primary: {error.diag.message_primary}
                detail: {error.diag.message_detail}
                context: {error.diag.context}
                internal: {error.diag.internal_query}
                severity: {error.diag.severity}
                table: {error.diag.table_name}
                ''',
            error_trace=None
        )


class PsycopgUniqueException(DatabaseException):
    def __init__(self, error: Error):
        super(PsycopgUniqueException, self).__init__(
            msg=f'''Unique Error:
                primary: {error.diag.message_primary}
                detail: {error.diag.message_detail}
                ''',
            error_trace=None
        )
