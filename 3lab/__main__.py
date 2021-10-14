#!/usr/bin/env python3

import argparse
import json
import os

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
resources_dir = os.path.join(script_dir, 'resources')


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


def parse_args():
    def file_exists(f):
        if not os.path.exists(f):
            raise argparse.ArgumentTypeError(f'{f} does no exist')
        return f

    parser = argparse.ArgumentParser()
    parser.add_argument('input_line', type=str,
                        help='input line for DFA')
    parser.add_argument('-f', '--file', type=file_exists, required=False,
                        default=os.path.join(resources_dir, 'dfa1.json'),
                        help='path to DFA json definition')
    return parser.parse_args()


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
            logging_list.add_action(current_state, ch, transit_to)
            current_state = transit_to
            input_list = input_list[1:]
        else:
            logging_list.set_error(f'no transition for symbol "{ch}" in state "{current_state}"')
            return logging_list

    if current_state not in dfa['end_states']:
        logging_list.set_error(f'input string ended at non end state "{current_state}"')
        return logging_list

    return logging_list


def main():
    args = parse_args()
    dfa_json_path = args.file
    input_line = args.input_line

    dfa = parse_dfa_json(dfa_json_path)
    verify_dfa(dfa)

    # TODO: refactor logging
    if 'info' in dfa:
        print(f'# [INFO]: {dfa["info"]}')
    logging_list = process_dfa(dfa, input_line)

    for log in logging_list:
        print(f'# [TRACE]: {log["from"]} --{log["symbol"]}--> {log["to"]}')
    if logging_list.has_error():
        print(f'# [ERROR]: {logging_list.get_error()}')


if __name__ == '__main__':
    main()
