import os
import sys

from dfa import parse_dfa_json, DFA
from util import DfaLoggingList

script_path = os.path.abspath(sys.argv[0])
script_dir = os.path.dirname(script_path)
resources_dir = os.path.join(script_dir, 'resources')


def cli_print_dfa_info(dfa):
    print(f'# [INFO]:  {dfa.get_info()}')


def cli_log_result(logging_list: DfaLoggingList):
    for event in logging_list:
        print(f'# [TRACE]: {event.from_state} --{event.symbol}--> {event.to_state}')
    if logging_list.has_error():
        print(f'# [ERROR]: {logging_list.get_error()}')


def cli_main(args):
    dfa_json_path = args.file or os.path.join(resources_dir, 'dfa1.json')
    input_lines = args.input_lines

    dfa_dict = parse_dfa_json(dfa_json_path)
    dfa = DFA(dfa_dict)

    if dfa.has_info():
        cli_print_dfa_info(dfa)

    for line in input_lines:
        print(f'\n# [INFO]:  Processing "{line}"')
        dfa.reset()
        dfa.start(line)
        dfa.process()
        logging_list = dfa.get_logging_list()
        cli_log_result(logging_list)
