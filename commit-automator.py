# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-10-27


import os
import json
import itertools
import subprocess
from typing import Union, Final
from datetime import datetime

import httpx


def getGithubData(*, user_name: str, access_token: str) -> dict:
    with httpx.Client() as client:
        url = "https://api.github.com/graphql"
        headers = {
            "Content-Type": "application/graphql",
            "Authorization": "Bearer " + access_token,
        }
        body = f"""
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

        response = client.post(url=url, headers=headers, json={"query": body})

    if response.status_code == 200:
        result = response.json()["data"]["user"]["contributionsCollection"][
            "contributionCalendar"
        ]["weeks"]
        contribution_days = [
            values for element in result for values in element.values()
        ]
        contribution_days = list(itertools.chain(*contribution_days))

        github_data = {
            element.get("date"): int(element.get("contributionCount"))
            for element in contribution_days
            if element.get("date")
        }

        return github_data
    else:
        raise ValueError(f"'status_code' is {response.status_code}!")


def getArtData(*, art_path: str) -> dict:
    with open(art_path) as f:
        art_data = json.load(f)

    start_day = datetime.strptime(art_data["start_date"], "%Y-%m-%d").strftime("%a")
    if start_day != "Sun":
        raise ValueError("'start_date' must start from Sunday!")

    if art_data["duration"] != len(art_data["pixels_level"]):
        raise ValueError("'duration' must be same with 'pixels_level'!")

    return art_data


def getDateDelta(*, art_file: str, today: str, start_date: str) -> int:
    today = datetime.strptime(today, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    date_delta = (today - start_date).days

    if date_delta < 0:
        raise ValueError(
            f"'start_date' of '{art_file}' must be earlier than or equal to today!"
        )

    return date_delta


def getPixelLevel(*, date_delta: int, pixels_level: list) -> int:
    flatten_pixels_level = list(itertools.chain(*pixels_level))
    total_pixels = len(flatten_pixels_level)
    pixel_idx = date_delta % total_pixels
    pixel_level = flatten_pixels_level[pixel_idx]

    return pixel_level


def getCommitCount(*, pixel_level: int, date_count: Union[int, None]) -> int:
    if date_count is not None:
        if date_count < 1:
            date_level = 0
        elif date_count < 15:
            date_level = 1
        elif date_count < 30:
            date_level = 2
        elif date_count < 45:
            date_level = 3
        else:
            date_level = 4
    else:
        raise ValueError("Cannot find commit count in Github now.. try later.")

    if pixel_level > date_level:
        if pixel_level == 1:
            min_commit = 1
        elif pixel_level == 2:
            min_commit = 15
        elif pixel_level == 3:
            min_commit = 30
        else:
            min_commit = 45

        commit_count = min_commit - date_count
    else:
        raise ValueError("Enough today.. nothing to commit.")

    return commit_count


def commitAndPush(*, art_name: str, commit_count: int) -> None:
    for count in range(commit_count):
        print(f"Auto Commit: {count + 1}")
        subprocess.call("echo commit-automator >>commit-automator.txt", shell=True)
        subprocess.call("git add commit-automator.txt", shell=True)
        subprocess.call(f"git commit -m 'auto: Run commit-automator for {art_name}'", shell=True)

    subprocess.call("rm commit-automator.txt", shell=True)
    subprocess.call("git add commit-automator.txt", shell=True)
    subprocess.call(f"git commit -m 'auto: commit-automator for {art_name}'", shell=True)
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
