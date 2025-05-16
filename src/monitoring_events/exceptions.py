from exceptions import ItemNotFound


class GeneralStatusNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(GeneralStatusNotFound, self).__init__(
            msg="Status context not found")


class MonitoringEventNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(MonitoringEventNotFound, self).__init__(
            msg="Event not found")
