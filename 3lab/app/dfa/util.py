import json


def parse_dfa_json(json_path):
    with open(json_path, 'r') as dfa_file:
        return json.load(dfa_file)


def verify_dfa_dict(dfa_dict):
    if 'states' not in dfa_dict \
            or type(dfa_dict['states']) != list \
            or len(dfa_dict['states']) <= 0:
        raise ValueError('"states" array is not defined or empty')

    if 'symbols' not in dfa_dict \
            or type(dfa_dict['symbols']) != list \
            or len(dfa_dict['states']) <= 0:
        raise ValueError('"symbols" array is not defined or empty')

    if 'start_state' not in dfa_dict \
            or type(dfa_dict['start_state']) != str \
            or dfa_dict['start_state'] not in dfa_dict['states']:
        raise ValueError('"start_state" is not defined or "start_state" not found in "states"')

    if 'end_states' not in dfa_dict \
            or type(dfa_dict['end_states']) != list \
            or len(dfa_dict['end_states']) <= 0 \
            or not all([True if state in dfa_dict['states'] else False for state in dfa_dict['end_states']]):
        raise ValueError('"end_states" is not defined or some state from "end_states" not found in "states"')

    if 'transitions' not in dfa_dict \
            or type(dfa_dict['transitions']) != list \
            or len(dfa_dict['transitions']) <= 0:
        raise ValueError('"transitions" is not defined')

    for state in dfa_dict['states']:
        if state in dfa_dict['symbols']:
            raise ValueError(f'literal "{state}" is present in both "states" and "symbols"')

    for transition in dfa_dict['transitions']:
        if 'from' not in transition \
                or type(transition['from']) != str \
                or transition['from'] not in dfa_dict['states']:
            raise ValueError('"from" is not defined or unknown state')

        if 'to' not in transition \
                or type(transition['to']) != str \
                or transition['to'] not in dfa_dict['states']:
            raise ValueError('"to" is not defined or unknown state')

        if 'symbols' not in transition \
                or type(transition['symbols']) != list \
                or len(transition['symbols']) <= 0 \
                or not all([True if symbol in dfa_dict['symbols'] else False for symbol in transition['symbols']]):
            raise ValueError('"symbols" is not defined or empty or not found in dfa "symbols"')
