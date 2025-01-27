from exceptions import ItemBusinessError, ItemNotFound


class MonitoredUrlNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoredUrlNotFound, self).__init__(
            msg=msg or "URL not found", error_trace=error_trace)


class MonitoredUrlBusinessError(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoredUrlBusinessError, self).__init__(
            msg=msg or "Could not service URL request", error_trace=error_trace)
