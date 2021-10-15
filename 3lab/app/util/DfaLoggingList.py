class DfaLoggingList:
    def __init__(self):
        self.__list = []
        self.__error = None

    def add_action(self, from_state, symbol, to_state):
        if not self.has_error():
            self.__list.append({
                'from': from_state,
                'symbol': symbol,
                'to': to_state,
            })

    def get_actions(self):
        return self.__list

    def set_error(self, error_text):
        self.__error = error_text

    def get_error(self):
        return self.__error

    def has_error(self):
        return True if self.__error is not None else False

    def __iter__(self):
        for entry in self.__list:
            yield entry
