# -*- coding=utf-8 -*-
r"""

"""
import os
import logging
import typing as t
import loggext
import configlib


def load_configuration() -> None:
    configlib.config.update(
        configlib.find_and_load_all(
            "/etc/t4search/config.{yml,yaml}",
            os.getenv("CONFIG_FILE", default=""),
            places=[],
        ),
    )
    configlib.config.update(
        configlib.loading.load_env(prefix="T4SEARCH")
    )


SHORT_LOGGING_FORMAT = "{asctime} | {levelname:.3} | {name:<30} | {message}"
LONG_LOGGING_FORMAT = "{asctime} | {levelname:.3} | {name} | {module} | {funcName} | {lineno} | {message}"
DEFAULT_DATEFORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging() -> None:
    handlers: t.List[logging.Handler] = []

    logging_format = _get_format()
    date_format = DEFAULT_DATEFORMAT
    level = getattr(logging, configlib.config.get('logging', 'level', converter=str.upper, fallback="INFO"))

    if loggext.is_running_in_shell():
        handlers.append(
            loggext.handlers.ColoredConsoleHandler()
        )
    else:
        handlers.append(
            logging.StreamHandler()
        )

    logging.basicConfig(
        style='{',
        format=logging_format,
        datefmt=date_format,
        level=level,
        handlers=handlers,
    )


def _get_format() -> str:
    fmt = configlib.config.get('logging', 'format', fallback="@SHORT")
    if fmt == "@SHORT":
        return SHORT_LOGGING_FORMAT
    elif fmt == "@LONG":
        return LONG_LOGGING_FORMAT
    else:
        return fmt
