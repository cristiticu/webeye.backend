from exceptions import ItemBusinessError, ItemNotFound


class MonitoredWebpageNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoredWebpageNotFound, self).__init__(
            msg=msg or "Webpage not found", error_trace=error_trace)


class MonitoredWebpageBusinessError(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoredWebpageBusinessError, self).__init__(
            msg=msg or "Could not perform webpage request", error_trace=error_trace)
