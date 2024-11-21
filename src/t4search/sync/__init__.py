# -*- coding=utf-8 -*-
r"""

"""
from pathlib import Path
from datetime import datetime


def __main__():
    now = datetime.now().isoformat()
    with Path("/var/log/cron.log").open('a') as file:
        file.write(f"Sync Job executed at {now}\n")
