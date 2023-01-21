# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import argparse
import os
import sys
from typing import Union

from __version__ import __version__
from actions import FileAction
from calculator import getCommitCount
from committer import commitAndPush
from dataloader import getGithubData
from logger import log, saveLog
from painter import displayArt


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="commit-automator",
        description="Check number of commits needed, and then commit & push it automatically.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action=FileAction,
        type=str,
        required=True,
        help="Filename of art.",
    )
    parser.add_argument(
        "-x",
        "--execute",
        choices=["commit", "display"],
        default="commit",
        help="Execute Commit or Display. Default is 'commit'.",
    )
    parser.add_argument(
        "-l",
        "--save-log",
        action="store_true",
        default=False,
        dest="is_save_log",
        help="Save log file 'automator.log'. Default is 'False'.",
    )
    args: argparse.Namespace = parser.parse_args()

    if args.is_save_log:
        saveLog()

    art_data: dict = FileAction.art_data

    if args.execute == "commit":
        env_name: str = "githubAccessToken"
        access_token: Union[str, None] = None

        try:
            access_token = os.environ[env_name]

            if access_token == "" or access_token is None:
                raise KeyError
        except KeyError:
            log.error(
                msg=f"Invalid value of '{env_name}': {access_token}\n"
                f"'{env_name}' must be already set in environment variables!\n\n\n"
                "[ Manually ] Run the folowwing example command:\n\n"
                f'  export {env_name}="YourGithubAccessToken"\n\n'
                "[ Automatically ] Write the fowllowing example line into Crontab:\n\n"
                f'  {env_name}="YourGithubAccessToken"\n\n\n'
                "If you have no Github access token, see here:\n\n"
                "  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
            )
            sys.exit(1)

        user_name: str = art_data["user_name"]
        github_data: dict = getGithubData(
            user_name=user_name, access_token=access_token
        )
        commit_count: int = getCommitCount(art_data=art_data, github_data=github_data)

        commitAndPush(commit_count=commit_count)

    if args.execute == "display":
        displayArt(art_data=art_data)


if __name__ == "__main__":
    main()
