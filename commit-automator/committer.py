# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import subprocess
import sys

from logger import log


def commitAndPush(*, commit_count: int) -> None:
    try:
        _lines: str = f""

        for _count in range(commit_count):
            subprocess.call("echo commit-automator >>commit-automator.txt", shell=True)
            subprocess.call("git add commit-automator.txt", shell=True)
            subprocess.call("git commit -m 'auto: run commit-automator'", shell=True)

            _lines += f"Auto Commit: {_count + 1}\n"

        subprocess.call("rm commit-automator.txt", shell=True)
        subprocess.call("git add commit-automator.txt", shell=True)
        subprocess.call("git commit -m 'auto: run commit-automator'", shell=True)
        subprocess.call("git push", shell=True)

        _lines += f"Nice.. done."

        log.info(msg=_lines)
    except:
        log.error(msg=f"Cannot commit and push.. Something's wrong!")
        sys.exit(1)
