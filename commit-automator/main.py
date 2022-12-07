# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Union

from calculator import getCommitCount, getDateDelta, getPixelLevel
from committer import commitAndPush
from dataloader import getArtData, getGithubData
from __version__ import __version__


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="commit-automator",
        description="Check number of commits needed, and then commit & push it automatically.",
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        required=True,
        help="Username of Github.",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Filename of art.",
    )
    parser.add_argument(
        "-x",
        "--execute",
        choices=["commit", "display"],
        required=True,
        help="Execute Commit or Display.",
    )

    args = parser.parse_args()

    key_name = "myGithubAccessToken"
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

    parent_dir: Path = Path(__file__).parents[1].absolute()
    art_path: Path = parent_dir / args.file
    art_data: dict = getArtData(art_path=art_path)

    if args.execute == "commit":
        github_data: dict = getGithubData(
            user_name=args.user, access_token=access_token
        )

        today: str = datetime.today().strftime("%Y-%m-%d")
        start_date: str = art_data["start_date"]
        date_delta: int = getDateDelta(
            art_file=args.file, today=today, start_date=start_date
        )

        pixels_level: list = art_data["pixels_level"]
        pixel_level: int = getPixelLevel(
            date_delta=date_delta, pixels_level=pixels_level
        )

        print(f"Today: {datetime.now()}")
        date_count: Union[int, None] = github_data.get(today, None)
        print(f"Github commits today: {date_count}")
        commit_count: int = getCommitCount(
            pixel_level=pixel_level, date_count=date_count
        )
        print(f"Need to commit more: {commit_count}")

        art_name: str = art_data["name"]
        commitAndPush(art_name=art_name, commit_count=commit_count)
    elif args.execute == "display":
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
