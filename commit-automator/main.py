# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import argparse
import os
import sys
from typing import Union

from __version__ import __version__
from actions import FileAction
from calculator import get_commit_count
from committer import commit_and_push
from dataloader import get_github_data
from logger import log, save_log
from painter import display_art


def main() -> None:
    _parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="commit-automator",
        description="Check number of commits needed, and then commit & push it automatically.",
    )
    _parser.add_argument(
        "-f",
        "--file",
        action=FileAction,
        type=str,
        required=True,
        help="Filename of art.",
    )
    _parser.add_argument(
        "-x",
        "--execute",
        choices=["commit", "display"],
        default="commit",
        help="Execute Commit or Display. Default is 'commit'.",
    )
    _parser.add_argument(
        "-l",
        "--save-log",
        action="store_true",
        default=False,
        dest="is_save_log",
        help="Save log file 'automator.log'. Default is 'False'.",
    )
    _args: argparse.Namespace = _parser.parse_args()

    if _args.is_save_log:
        save_log()

    _art_data: dict = FileAction.art_data

    if _args.execute == "commit":
        _env_name: str = "githubAccessToken"
        _access_token: Union[str, None] = None

        try:
            _access_token = os.environ[_env_name]

            if _access_token == "" or _access_token is None:
                raise KeyError
        except KeyError:
            log.error(
                msg=f"Invalid value of '{_env_name}': {_access_token}\n"
                f"'{_env_name}' must be already set in environment variables!\n\n\n"
                "[ Manually ] Run the folowwing example command:\n\n"
                f'  export {_env_name}="YourGithubAccessToken"\n\n'
                "[ Automatically ] Write the fowllowing example line into Crontab:\n\n"
                f'  {_env_name}="YourGithubAccessToken"\n\n\n'
                "If you have no Github access token, see here:\n\n"
                "  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
            )
            sys.exit(1)

        _user_name: str = _art_data["user_name"]
        _github_data: dict = get_github_data(
            user_name=_user_name, access_token=_access_token
        )
        _commit_count: int = get_commit_count(
            art_data=_art_data, github_data=_github_data
        )

        commit_and_push(commit_count=_commit_count)

    if _args.execute == "display":
        display_art(art_data=_art_data)


if __name__ == "__main__":
    main()
