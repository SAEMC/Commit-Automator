# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

from argparse import ArgumentParser, Namespace
from os import environ
from sys import exit
from typing import Union

from src.__version__ import __version__
from src.actions import FileAction
from src.argparsers import AppArgParser
from src.calculator import get_commit_count
from src.committer import commit_and_push
from src.dataloader import get_github_data
from src.logger import logger, save_log
from src.painter import display_art


def _get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="src",
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
        dest="execute",
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

    return parser


def main() -> None:
    _parser: ArgumentParser = _get_parser()
    _namespace: Namespace = _parser.parse_args()
    _args: AppArgParser = AppArgParser(namespace=_namespace)

    _save_log_is_in_args: bool = _args.is_save_log

    if _save_log_is_in_args:
        save_log()

    _art_data: dict[str, Union[int, list[list[int]]], str] = FileAction.art_data
    _excution_is_commitment: bool = _args.execute == "commit"
    _excution_is_display: bool = _args.execute == "display"

    if _excution_is_commitment:
        _env_name: str = "githubAccessToken"
        _access_token: Union[str, None] = None

        try:
            _access_token = environ[_env_name]
            _access_token_is_empty_string_or_none: bool = (
                _access_token == "" or _access_token is None
            )

            if _access_token_is_empty_string_or_none:
                raise KeyError
        except KeyError:
            logger.error(
                msg=f"Invalid value of '{_env_name}': {_access_token}\n"
                f"'{_env_name}' must be already set in environment variables!\n\n\n"
                "[ Manually ] Run the folowwing example command:\n\n"
                f'  export {_env_name}="YourGithubAccessToken"\n\n'
                "[ Automatically ] Write the fowllowing example line into Crontab:\n\n"
                f'  {_env_name}="YourGithubAccessToken"\n\n\n'
                "If you have no Github access token, see here:\n\n"
                "  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
            )
            exit(1)

        _user_name: str = _art_data["user_name"]
        _github_data: dict[str, int] = get_github_data(
            user_name=_user_name, access_token=_access_token
        )
        _commit_count: int = get_commit_count(
            art_data=_art_data, github_data=_github_data
        )

        commit_and_push(commit_count=_commit_count)

    if _excution_is_display:
        display_art(art_data=_art_data)


if __name__ == "__main__":
    main()
