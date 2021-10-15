import json

from util import DfaLoggingList, DfaLoggingEvent


def parse_dfa_json(json_path):
    with open(json_path, 'r') as dfa_file:
        return json.load(dfa_file)


def verify_dfa(dfa):
    if 'states' not in dfa \
            or type(dfa['states']) != list \
            or len(dfa['states']) <= 0:
        raise ValueError('"states" array is not defined or empty')

    if 'symbols' not in dfa \
            or type(dfa['symbols']) != list \
            or len(dfa['states']) <= 0:
        raise ValueError('"symbols" array is not defined or empty')

    if 'start_state' not in dfa \
            or type(dfa['start_state']) != str \
            or dfa['start_state'] not in dfa['states']:
        raise ValueError('"start_state" is not defined or "start_state" not found in "states"')

    if 'end_states' not in dfa \
            or type(dfa['end_states']) != list \
            or len(dfa['end_states']) <= 0 \
            or not all([True if state in dfa['states'] else False for state in dfa['end_states']]):
        raise ValueError('"end_states" is not defined or some state from "end_states" not found in "states"')

    if 'transitions' not in dfa \
            or type(dfa['transitions']) != list \
            or len(dfa['transitions']) <= 0:
        raise ValueError('"transitions" is not defined')

    for state in dfa['states']:
        if state in dfa['symbols']:
            raise ValueError(f'literal "{state}" is present in both "states" and "symbols"')

    for transition in dfa['transitions']:
        if 'from' not in transition \
                or type(transition['from']) != str \
                or transition['from'] not in dfa['states']:
            raise ValueError('"from" is not defined or unknown state')

        if 'to' not in transition \
                or type(transition['to']) != str \
                or transition['to'] not in dfa['states']:
            raise ValueError('"to" is not defined or unknown state')

        if 'symbols' not in transition \
                or type(transition['symbols']) != list \
                or len(transition['symbols']) <= 0 \
                or not all([True if symbol in dfa['symbols'] else False for symbol in transition['symbols']]):
            raise ValueError('"symbols" is not defined or empty or not found in dfa "symbols"')


def process_dfa(dfa, input_str):
    logging_list = DfaLoggingList()

    def verify_input():
        for symbol in input_str:
            if symbol not in dfa['symbols']:
                logging_list.set_error(f'input contains wrong symbol "{symbol}"')

    def current_state_transition(symbol):
        for transition in dfa['transitions']:
            if transition['from'] == current_state and symbol in transition['symbols']:
                return transition['to']
        return None

    verify_input()
    if logging_list.has_error():
        return logging_list

    current_state = dfa['start_state']
    input_list = list(input_str)
    while len(input_list) > 0:
        ch = input_list[0]
        transit_to = current_state_transition(ch)
        if transit_to:
            logging_list.add_event(DfaLoggingEvent(current_state, ch, transit_to))
            current_state = transit_to
            input_list = input_list[1:]
        else:
            logging_list.set_error(f'no transition for symbol "{ch}" in state "{current_state}"')
            return logging_list

    if current_state not in dfa['end_states']:
        logging_list.set_error(f'input string ended at non end state "{current_state}"')
        return logging_list

    return logging_list
