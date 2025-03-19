from exceptions import ItemNotFound


class LoggedInDeviceNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(LoggedInDeviceNotFound, self).__init__(
            msg=msg or "Invalid device", error_trace=error_trace)
