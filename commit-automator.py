# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-10-27


import os
import itertools
from typing import Union
from datetime import datetime

import httpx
import json
from bs4 import BeautifulSoup as bs


def get_github(url: str) -> dict:
    page = httpx.get(url)
    soup = bs(page.text, "html.parser")
    calendar = soup.find_all("rect", {"class": "ContributionCalendar-day"})

    return {
        e.get("data-date"): int(e.get("data-count"))
        for e in calendar
        if e.get("data-date")
    }


def get_art(art_path: str) -> dict:
    with open(art_path) as f:
        data = json.load(f)

    start_day = datetime.strptime(data["start_date"], "%Y-%m-%d").strftime("%a")
    if start_day != "Sun":
        raise ValueError("'start_date' must start from Sunday!")

    if data["duration"] != len(data["pixels_level"]):
        raise ValueError("'duration' must be same with 'pixels_level'!")

    return data


def get_date_delta(today: str, start_date: str) -> int:
    today = datetime.strptime(today, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    date_delta = (today - start_date).days

    if date_delta < 0:
        raise ValueError("'date_delta' must be greater than or equal to 0!")

    return date_delta


def get_pixel_level(date_delta: int, pixels_level: list) -> int:
    flatten_pixels_level = list(itertools.chain(*pixels_level))
    total_pixels = len(flatten_pixels_level)
    pixel_idx = date_delta % total_pixels
    pixel_level = flatten_pixels_level[pixel_idx]

    return pixel_level


def get_commit_num(pixel_level: int, date_count: Union[int, None]) -> int:
    if date_count:
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
        raise ValueError("'date_count' must be int!")

    if pixel_level > date_level:
        if pixel_level == 1:
            min_commit = 1
        elif pixel_level == 2:
            min_commit = 15
        elif pixel_level == 3:
            min_commit = 30
        else:
            min_commit = 45

        need_to_commit = min_commit - date_count
    else:
        raise ValueError("Nothing to commit!")

    return need_to_commit


def auto_commit(need_to_commit: int) -> None:
    for count in range(need_to_commit):
        print(f"Auto Commit: {count + 1}")
        os.system("echo commit-automator >>commit-automator.txt")
        os.system("git add commit-automator.txt")
        os.system("git commit -m 'auto commit'")

    os.system("rm commit-automator.txt")
    os.system("git add commit-automator.txt")
    os.system("git commit -m 'auto commit'")
    os.system("git push")
    print(f"Done!")


def main():
    github_data = get_github("https://github.com/SAEMC/")
    art_data = get_art("art.json")

    today = datetime.today().strftime("%Y-%m-%d")
    start_date = art_data["start_date"]
    date_delta = get_date_delta(today, start_date)

    pixels_level = art_data["pixels_level"]
    pixel_level = get_pixel_level(date_delta, pixels_level)

    date_count = github_data.get(today, None)
    print(f"Github commits: {date_count}")
    need_to_commit = get_commit_num(pixel_level, date_count)
    print(f"Need to commit: {need_to_commit}")

    auto_commit(need_to_commit)


if __name__ == "__main__":
    main()
