# -*- coding=utf-8 -*-
r"""

"""
import importlib
import typing as t
import argparse as ap
try:
    import better_exceptions
except ModuleNotFoundError:
    pass
else:
    better_exceptions.hook()

parser = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers(dest="__main__")

api_parser = subparsers.add_parser(name="api", formatter_class=ap.ArgumentDefaultsHelpFormatter)

sync_parser = subparsers.add_parser(name="sync", formatter_class=ap.ArgumentDefaultsHelpFormatter)

reset_parser = subparsers.add_parser(name="reset", formatter_class=ap.ArgumentDefaultsHelpFormatter)


def main(argv: t.List[str] = None) -> int:
    from .conf import load_configuration, configure_logging

    arguments = vars(parser.parse_args(argv))
    __main__ = arguments.pop('__main__')
    load_configuration()
    configure_logging()
    submodule = importlib.import_module(f".{__main__}", package=__package__)
    submodule.__main__(**arguments)
    return 0


if __name__ == '__main__':
    exit(main() or 0)
