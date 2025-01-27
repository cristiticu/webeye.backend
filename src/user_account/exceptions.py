from exceptions import ItemCreateError, ItemNotFound


class UserAccountNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(UserAccountNotFound, self).__init__(
            msg=msg or "User Account not found", error_trace=error_trace)


class UserCreateError(ItemCreateError):
    def __init__(self, msg=None, error_trace=None):
        super(UserCreateError, self).__init__(
            msg=msg or "Could not create user account", error_trace=error_trace)
