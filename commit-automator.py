# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-10-27


import os
import itertools
import json
import subprocess
from datetime import datetime
from typing import Union, Final

import httpx


def getGithubData(*, user_name: str, access_token: str) -> dict:
    with httpx.Client() as _client:
        _url = "https://api.github.com/graphql"
        _headers = {
            "Content-Type": "application/graphql",
            "Authorization": "Bearer " + access_token,
        }
        _body = f"""
        query {{
            user(login: "{user_name}") {{
                contributionsCollection {{
                    contributionCalendar {{
                        totalContributions weeks {{
                            contributionDays {{
                                contributionCount date
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """

        _response = _client.post(url=_url, headers=_headers, json={"query": _body})

    if _response.status_code == 200:
        _result = _response.json()["data"]["user"]["contributionsCollection"][
            "contributionCalendar"
        ]["weeks"]
        _contribution_days = [
            _values for _element in _result for _values in _element.values()
        ]
        _contribution_days = list(itertools.chain(*_contribution_days))

        _github_data = {
            _element.get("date"): int(_element.get("contributionCount"))
            for _element in _contribution_days
            if _element.get("date")
        }

        return _github_data
    else:
        raise ValueError(f"'status_code' is {_response.status_code}!")


def getArtData(*, art_path: str) -> dict:
    with open(art_path) as f:
        _art_data = json.load(f)

    _start_date = datetime.strptime(_art_data["start_date"], "%Y-%m-%d").strftime("%a")
    if _start_date != "Sun":
        raise ValueError("'start_date' must start from Sunday!")

    if _art_data["duration"] != len(_art_data["pixels_level"]):
        raise ValueError("'duration' must be same with 'pixels_level'!")

    return _art_data


def getDateDelta(*, art_file: str, today: str, start_date: str) -> int:
    _today = datetime.strptime(today, "%Y-%m-%d")
    _start_date = datetime.strptime(start_date, "%Y-%m-%d")
    _date_delta = (_today - _start_date).days

    if _date_delta < 0:
        raise ValueError(
            f"'start_date' of '{art_file}' must be earlier than or equal to today!"
        )

    return _date_delta


def getPixelLevel(*, date_delta: int, pixels_level: list) -> int:
    _flatten_pixels_level = list(itertools.chain(*pixels_level))
    _total_pixels = len(_flatten_pixels_level)
    _pixel_idx = date_delta % _total_pixels
    _pixel_level = _flatten_pixels_level[_pixel_idx]

    return _pixel_level


def getCommitCount(*, pixel_level: int, date_count: Union[int, None]) -> int:
    if date_count is not None:
        if date_count < 1:
            _date_level = 0
        elif date_count < 15:
            _date_level = 1
        elif date_count < 30:
            _date_level = 2
        elif date_count < 45:
            _date_level = 3
        else:
            _date_level = 4
    else:
        raise ValueError("Cannot find commit count in Github now.. try later.")

    if pixel_level > _date_level:
        if pixel_level == 1:
            _min_commit = 1
        elif pixel_level == 2:
            _min_commit = 15
        elif pixel_level == 3:
            _min_commit = 30
        else:
            _min_commit = 45

        _commit_count = _min_commit - date_count
    else:
        raise ValueError("Enough today.. nothing to commit.")

    return _commit_count


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


def main() -> None:
    USER_NAME: Final = "SAEMC"
    ART_FILE: Final = "art.json"

    abs_path: str = os.path.abspath(__file__)
    abs_dir: str = os.path.dirname(abs_path)
    access_token: str = os.environ["myGithubAccessToken"]
    art_path: str = os.path.join(abs_dir, ART_FILE)

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
