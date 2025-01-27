from exceptions import ItemBusinessError, ItemNotFound


class UserAccountNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(UserAccountNotFound, self).__init__(
            msg=msg or "User Account not found", error_trace=error_trace)


class UserBusinessError(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(UserBusinessError, self).__init__(
            msg=msg or "Could not service user account request", error_trace=error_trace)
