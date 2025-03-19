from exceptions import ItemNotFound


class ScheduledTaskNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(ScheduledTaskNotFound, self).__init__(
            msg=msg or "Task not found", error_trace=error_trace)
