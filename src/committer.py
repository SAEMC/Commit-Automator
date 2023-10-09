# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

from subprocess import call
from sys import exit

from src.logger import logger


def commit_and_push(*, commit_count: int) -> None:
    try:
        _lines: str = f""

        for _count in range(commit_count):
            call("echo commit-automator >>commit-automator.txt", shell=True)
            call("git add commit-automator.txt", shell=True)
            call("git commit -m 'auto: run commit-automator'", shell=True)

            _lines += f"Auto Commit: {_count + 1}\n"

        call("rm commit-automator.txt", shell=True)
        call("git add commit-automator.txt", shell=True)
        call("git commit -m 'auto: run commit-automator'", shell=True)
        call("git push", shell=True)

        _lines += "Nice.. done."

        logger.info(msg=_lines)
    except:
        logger.error(msg="Cannot commit and push.. Something's wrong!")
        exit(1)
