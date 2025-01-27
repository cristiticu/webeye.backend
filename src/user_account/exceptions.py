from exceptions import ItemNotFound


class UserAccountNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(UserAccountNotFound, self).__init__(
            msg=msg or "User Account not found", error_trace=error_trace)
