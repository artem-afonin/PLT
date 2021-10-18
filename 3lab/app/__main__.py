from cli import cli_main
from gui import gui_main
from util import parse_args


def main():
    args = parse_args()
    if args.cli:
        cli_main(args)
    else:
        gui_main(args)


if __name__ == '__main__':
    main()
