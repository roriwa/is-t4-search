# -*- coding=utf-8 -*-
r"""

"""
import logging
from pathlib import Path
from ..core import create_chroma_client


def __main__():
    logging.info("resetting chroma")
    chroma_client = create_chroma_client()
    chroma_client.reset()

    logging.info("removing synced.json")
    Path.cwd().joinpath("synced.json").unlink(missing_ok=True)
