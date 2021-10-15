#!/usr/bin/env python3

from cli import cli_main
from util import parse_args


def main():
    args = parse_args()
    if args.cli:
        cli_main(args)
    else:
        pass


if __name__ == '__main__':
    main()
