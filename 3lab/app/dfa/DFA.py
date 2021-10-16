from enum import Enum
from typing import Optional

from dfa.util import verify_dfa_dict
from util import DfaLoggingList, DfaLoggingEvent


class DFAGlobalState(Enum):
    RESET = 1
    START = 2
    HALT = 3


class DFA:
    def __init__(self, dfa_dict: dict):
        verify_dfa_dict(dfa_dict)
        self.__dfa_dict = dfa_dict
        self.__logging_list = DfaLoggingList()
        self.__current_state = self.__dfa_dict['start_state']
        self.__global_state = DFAGlobalState.RESET
        self.__input_list = []

    def start(self, input_str):
        """ Pass new str to DFA and start it """
        if self.__global_state == DFAGlobalState.HALT:
            raise RuntimeError('can not start stopped DFA')
        elif self.__global_state == DFAGlobalState.START:
            return

        self.__verify_input(input_str)
        if self.__logging_list.has_error():
            self.halt()
            return
        self.__input_list = list(input_str)
        self.__global_state = DFAGlobalState.START

    def halt(self):
        """ Interrupt DFA execution (irretrievable action) """
        self.__global_state = DFAGlobalState.HALT

    def reset(self):
        """ Reset DFA state and prepare it for parsing new line """
        self.__current_state = self.__dfa_dict['start_state']
        self.__logging_list = DfaLoggingList()
        self.__global_state = DFAGlobalState.RESET

    def step(self):
        """ Execute single DFA transition """
        if self.__global_state != DFAGlobalState.START:
            raise RuntimeError('DFA is not started!')

        if len(self.__input_list) > 0:
            ch = self.__input_list[0]
            transit_to = self.__find_current_state_transition(ch)
            if transit_to:
                self.__logging_list.add_event(DfaLoggingEvent(self.__current_state, ch, transit_to))
                self.__current_state = transit_to
                self.__input_list = self.__input_list[1:]
            else:
                self.__logging_list.set_error(f'no transition for symbol "{ch}" in state "{self.__current_state}"')
                self.halt()
                return
        else:
            if self.__current_state not in self.__dfa_dict['end_states']:
                self.__logging_list.set_error(f'input string ended at non end state "{self.__current_state}"')
            self.halt()

    def process(self):
        """ Execute all DFA transitions from current to the halt """
        while self.__global_state != DFAGlobalState.HALT:
            self.step()

    def get_logging_list(self):
        """ Get DFA logging list """
        return self.__logging_list

    def has_info(self) -> bool:
        """ Check for DFA information """
        return 'info' in self.__dfa_dict

    def get_info(self) -> Optional[str]:
        """ Get DFA information """
        return self.__dfa_dict['info'] if self.has_info() else None

    def get_global_state(self) -> DFAGlobalState:
        """ Get current global DFA state """
        return self.__global_state

    def __verify_input(self, input_str):
        """ Check that input do not contains wrong symbols """
        for symbol in input_str:
            if symbol not in self.__dfa_dict['symbols']:
                self.__logging_list.set_error(f'input contains wrong symbol "{symbol}"')

    def __find_current_state_transition(self, symbol):
        """ Find transition from current state by symbol """
        for transition in self.__dfa_dict['transitions']:
            if transition['from'] == self.__current_state and symbol in transition['symbols']:
                return transition['to']
        return None
