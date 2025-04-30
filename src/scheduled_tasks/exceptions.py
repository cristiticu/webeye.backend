from exceptions import ItemBusinessError, ItemNotFound


class ScheduledTaskNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(ScheduledTaskNotFound, self).__init__(
            msg=msg or "Task not found", error_trace=error_trace)


class ScheduledCheckAlreadyExists(ItemBusinessError):
    def __init__(self, msg=None, error_trace=None):
        super(ScheduledCheckAlreadyExists, self).__init__(
            msg=msg or "Scheduled check already registered", error_trace=error_trace)
