from exceptions import ItemBusinessError, ItemNotFound


class MonitoredWebpageNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoredWebpageNotFound, self).__init__(
            msg=msg or "Webpage not found", error_trace=error_trace)


class MonitoredWebpageAlreadyExists(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoredWebpageAlreadyExists, self).__init__(
            msg=msg or "URL already monitored", error_trace=error_trace)


class UrlNotReachable(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(UrlNotReachable, self).__init__(
            msg=msg or "URL unreachable", error_trace=error_trace)
