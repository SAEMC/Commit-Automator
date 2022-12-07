# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import argparse
import os
import sys
from pathlib import Path

from calculator import getCommitCount
from committer import commitAndPush
from dataloader import getArtData, getGithubData
from painter import displayArt

from __version__ import __version__


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="commit-automator",
        description="Check number of commits needed, and then commit & push it automatically.",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="art.json",
        type=str,
        help="Filename of art. Default is 'art.json'.",
    )
    parser.add_argument(
        "-x",
        "--execute",
        choices=["commit", "display"],
        default="commit",
        help="Execute Commit or Display. Default is 'commit'.",
    )
    args = parser.parse_args()

    parent_dir: Path = Path(__file__).parents[1].absolute()
    art_path: Path = parent_dir / args.file
    art_data: dict = getArtData(art_path=art_path)

    if args.execute == "commit":
        key_name = "githubAccessToken"

        try:
            access_token: str = os.environ[key_name]
        except KeyError:
            print(
                f"'{key_name}' must be already set in environment variables!\n"
                f"Run folowwing example command first if you execute manually:\n\n"
                f' export {key_name}="TheValueOfGithubAccessToken"\n\n'
                f"Write fowllowing example line first into Crontab if you execute automatically:\n\n"
                f' {key_name}="TheValueOfGithubAccessToken"\n\n'
                f"If you have no Github access token, see here:\n"
                f"https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
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
