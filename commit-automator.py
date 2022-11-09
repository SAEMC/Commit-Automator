# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-10-27


import os
import json
import itertools
import subprocess
from typing import Union
from datetime import datetime

import httpx


def getGithubData(user_name: str, access_token: str) -> dict:
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

        return {
            element.get("date"): int(element.get("contributionCount"))
            for element in contribution_days
            if element.get("date")
        }
    else:
        raise ValueError(f"'status_code' is {response.status_code}!")


def getArtData(art_path: str) -> dict:
    with open(art_path) as f:
        data = json.load(f)

    start_day = datetime.strptime(data["start_date"], "%Y-%m-%d").strftime("%a")
    if start_day != "Sun":
        raise ValueError("'start_date' must start from Sunday!")

    if data["duration"] != len(data["pixels_level"]):
        raise ValueError("'duration' must be same with 'pixels_level'!")

    return data


def getDateDelta(today: str, start_date: str) -> int:
    today = datetime.strptime(today, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    date_delta = (today - start_date).days

    if date_delta < 0:
        raise ValueError("'start_date' of 'art.json' must be earlier than today !")

    return date_delta


def getPixelLevel(date_delta: int, pixels_level: list) -> int:
    flatten_pixels_level = list(itertools.chain(*pixels_level))
    total_pixels = len(flatten_pixels_level)
    pixel_idx = date_delta % total_pixels
    pixel_level = flatten_pixels_level[pixel_idx]

    return pixel_level


def getCommitCount(pixel_level: int, date_count: Union[int, None]) -> int:
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


def commitAndPush(art_name: str, commit_count: int) -> None:
    for count in range(commit_count):
        print(f"Auto Commit: {count + 1}")
        subprocess.call("echo commit-automator >>commit-automator.txt", shell=True)
        subprocess.call("git add commit-automator.txt", shell=True)
        subprocess.call(f"git commit -m 'Commit Automator for {art_name}'", shell=True)

    subprocess.call("rm commit-automator.txt", shell=True)
    subprocess.call("git add commit-automator.txt", shell=True)
    subprocess.call(f"git commit -m 'Commit Automator for {art_name}'", shell=True)
    subprocess.call("git push", shell=True)
    print(f"Nice.. done.")


def main():
    abs_path = os.path.abspath(__file__)
    abs_dir = os.path.dirname(abs_path)

    user_name = "SAEMC"
    access_token = os.environ["myGithubAccessToken"]

    github_data = getGithubData(user_name, access_token)
    art_data = getArtData(os.path.join(abs_dir, "art.json"))

    today = datetime.today().strftime("%Y-%m-%d")
    start_date = art_data["start_date"]
    date_delta = getDateDelta(today, start_date)

    pixels_level = art_data["pixels_level"]
    pixel_level = getPixelLevel(date_delta, pixels_level)

    date_count = github_data.get(today, None)
    print(f"Github commits today: {date_count}")
    commit_count = getCommitCount(pixel_level, date_count)
    print(f"Need to commit more: {commit_count}")

    art_name = art_data["name"]
    commitAndPush(art_name, commit_count)


if __name__ == "__main__":
    main()
