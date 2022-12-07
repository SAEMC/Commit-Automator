# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import subprocess


def commitAndPush(*, art_name: str, commit_count: int) -> None:
    for _count in range(commit_count):
        print(f"Auto Commit: {_count + 1}")
        subprocess.call("echo commit-automator >>commit-automator.txt", shell=True)
        subprocess.call("git add commit-automator.txt", shell=True)
        subprocess.call(
            f"git commit -m 'auto: Run commit-automator for {art_name}'", shell=True
        )

    subprocess.call("rm commit-automator.txt", shell=True)
    subprocess.call("git add commit-automator.txt", shell=True)
    subprocess.call(
        f"git commit -m 'auto: Run commit-automator for {art_name}'", shell=True
    )
    subprocess.call("git push", shell=True)
    print(f"Nice.. done.")
