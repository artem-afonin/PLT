import os
import sys

from dfa import parse_dfa_json, verify_dfa, process_dfa
from util import DfaLoggingList

script_path = os.path.abspath(sys.argv[0])
script_dir = os.path.dirname(script_path)
resources_dir = os.path.join(script_dir, 'resources')


def cli_print_dfa_info(dfa):
    print(f'# [INFO]:  {dfa["info"]}')


def cli_log_result(logging_list: DfaLoggingList):
    for event in logging_list:
        print(f'# [TRACE]: {event.from_state} --{event.symbol}--> {event.to_state}')
    if logging_list.has_error():
        print(f'# [ERROR]: {logging_list.get_error()}')


def cli_main(args):
    dfa_json_path = args.file or os.path.join(resources_dir, 'dfa1.json')
    input_line = args.input_line

    dfa = parse_dfa_json(dfa_json_path)
    verify_dfa(dfa)

    if 'info' in dfa:
        cli_print_dfa_info(dfa)

    logging_list = process_dfa(dfa, input_line)
    cli_log_result(logging_list)
