# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import subprocess

from logger import log


def commitAndPush(*, commit_count: int) -> None:
    for _count in range(commit_count):
        log.info(msg=f"Auto Commit: {_count + 1}")
        subprocess.call("echo commit-automator >>commit-automator.txt", shell=True)
        subprocess.call("git add commit-automator.txt", shell=True)
        subprocess.call(f"git commit -m 'auto: run commit-automator'", shell=True)

    subprocess.call("rm commit-automator.txt", shell=True)
    subprocess.call("git add commit-automator.txt", shell=True)
    subprocess.call(f"git commit -m 'auto: run commit-automator'", shell=True)
    subprocess.call("git push", shell=True)
    log.info(msg=f"Nice.. done.")
