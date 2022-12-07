# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import os
from datetime import datetime
from pathlib import Path
from typing import Union, Final


from calculator import getCommitCount, getDateDelta, getPixelLevel
from committer import commitAndPush
from dataloader import getArtData, getGithubData
from __version__ import __version__


def main() -> None:
    USER_NAME: Final = "SAEMC"
    ART_FILE: Final = "art.json"

    access_token: str = os.environ["myGithubAccessToken"]
    parent_dir: Path = Path(__file__).parents[1].absolute()
    art_path: Path = parent_dir / ART_FILE

    github_data: dict = getGithubData(user_name=USER_NAME, access_token=access_token)
    art_data: dict = getArtData(art_path=art_path)

    today: str = datetime.today().strftime("%Y-%m-%d")
    start_date: str = art_data["start_date"]
    date_delta: int = getDateDelta(
        art_file=ART_FILE, today=today, start_date=start_date
    )

    pixels_level: list = art_data["pixels_level"]
    pixel_level: int = getPixelLevel(date_delta=date_delta, pixels_level=pixels_level)

    print(f"Today: {datetime.now()}")
    date_count: Union[int, None] = github_data.get(today, None)
    print(f"Github commits today: {date_count}")
    commit_count: int = getCommitCount(pixel_level=pixel_level, date_count=date_count)
    print(f"Need to commit more: {commit_count}")

    art_name: str = art_data["name"]
    commitAndPush(art_name=art_name, commit_count=commit_count)


if __name__ == "__main__":
    main()
