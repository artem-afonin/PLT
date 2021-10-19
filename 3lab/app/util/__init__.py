import argparse
import os

from .DfaLoggingEvent import DfaLoggingEvent
from .DfaLoggingList import DfaLoggingList


def parse_args():
    def file_exists(f):
        if not os.path.exists(f):
            raise argparse.ArgumentTypeError(f'{f} does no exist')
        return f

    parser = argparse.ArgumentParser()

    parser.add_argument('input_lines', type=str, nargs='*',
                        help='input line for DFA')
    parser.add_argument('-f', '--file', type=file_exists, required=False,
                        help='path to DFA json definition')

    parser.add_argument('--cli', action='store_true', default=False,
                        help='run in CLI without GUI')

    return parser.parse_args()
