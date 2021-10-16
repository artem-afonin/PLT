class DfaLoggingEvent:
    def __init__(self, from_state, symbol, to_state):
        self.from_state = from_state
        self.symbol = symbol
        self.to_state = to_state
