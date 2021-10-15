from typing import List, Optional

from util import DfaLoggingEvent


class DfaLoggingList:
    def __init__(self):
        self.__event_list: List[DfaLoggingEvent] = []
        self.__error: Optional[str] = None

    def add_event(self, event: DfaLoggingEvent):
        if not self.has_error():
            self.__event_list.append(event)

    def get_events(self) -> List[DfaLoggingEvent]:
        return self.__event_list

    def set_error(self, error_text: str):
        self.__error = error_text

    def get_error(self) -> str:
        return self.__error

    def has_error(self) -> bool:
        return True if self.__error is not None else False

    def __iter__(self):
        for entry in self.__event_list:
            yield entry
