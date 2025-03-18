from exceptions import ItemBusinessError, ItemNotFound


class UserAccountNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(UserAccountNotFound, self).__init__(
            msg=msg or "User Account not found", error_trace=error_trace)


class EmailAlreadyExists(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(EmailAlreadyExists, self).__init__(
            msg=msg or "Email already registered", error_trace=error_trace)
