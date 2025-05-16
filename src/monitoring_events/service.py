from datetime import datetime
from monitoring_events.persistence import MonitoringEventsPersistence


class MonitoringEventsService():
    def __init__(self, persistence: MonitoringEventsPersistence):
        self._events = persistence

    def get_general_status(self, u_guid: str, url: str):
        return self._events.get_general_status(u_guid, url)

    def get_regions_status(self, u_guid: str, url: str):
        return self._events.get_regions_status(u_guid, url)

    def get_event(self, u_guid: str, url: str, c_at: str):
        return self._events.get_event(u_guid, url, c_at)

    def get_events(self, u_guid: str, url: str, last_evaluated_key: str | None = None):
        return self._events.get_events(
            u_guid,
            url,
            last_evaluated_key
        )

    def get_downtimes(self, u_guid: str, url: str, start_at: str, end_at: str):
        return self._events.get_downtimes(
            u_guid,
            url,
            start_at,
            end_at
        )
