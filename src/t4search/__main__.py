# -*- coding=utf-8 -*-
r"""

"""
import os
import importlib
import typing as t
import argparse as ap
import configlib
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


def main(argv: t.List[str] = None) -> int:
    from .logging import configure as configure_logging

    arguments = vars(parser.parse_args(argv))
    __main__ = arguments.pop('__main__')
    config_file = os.getenv("CONFIG_FILE")
    if config_file:
        configlib.config.update(configlib.load(config_file))
    configure_logging()
    submodule = importlib.import_module(f".{__main__}", package=__package__)
    submodule.__main__(**arguments)
    return 0


if __name__ == '__main__':
    exit(main() or 0)
