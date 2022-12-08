# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import sys
from datetime import datetime
from typing import Union


def _calDateDelta(*, today: str, start_date: str) -> int:
    _today: datetime = datetime.strptime(today, "%Y-%m-%d")
    _start_date: datetime = datetime.strptime(start_date, "%Y-%m-%d")
    _date_delta: int = (_today - _start_date).days

    try:
        if _date_delta < 0:
            raise ValueError(f"'start_date' must be earlier than or equal to today!")
    except ValueError as e:
        print(e)
        sys.exit(1)

    return _date_delta


def _calPixelLevel(*, date_delta: int, pixels_level: list) -> int:
    _flatten_pixels_level: list = list(itertools.chain(*pixels_level))

    _wrong_pixels_level = [
        _level for _level in _flatten_pixels_level if _level < 0 or _level > 4
    ]

    try:
        if _wrong_pixels_level:
            raise ValueError(f"The value of 'pixels_level' must be '0' ~ '4'!")
    except ValueError as e:
        print(e)
        sys.exit(1)

    _total_pixels: int = len(_flatten_pixels_level)
    _pixel_idx: int = date_delta % _total_pixels
    _pixel_level: int = _flatten_pixels_level[_pixel_idx]

    return _pixel_level


def _calCommitCount(*, pixel_level: int, date_count: Union[int, None]) -> int:
    _date_level: int
    _min_commit: int

    try:
        if date_count is None:
            raise ValueError("Cannot find commit count in Github now.. try later.")
    except ValueError as e:
        print(e)
        sys.exit(1)

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

    try:
        if pixel_level <= _date_level:
            raise ValueError("Enough today.. nothing to commit.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    if pixel_level == 1:
        _min_commit = 1
    elif pixel_level == 2:
        _min_commit = 15
    elif pixel_level == 3:
        _min_commit = 30
    else:
        _min_commit = 45

    _commit_count: int = _min_commit - date_count

    return _commit_count


def getCommitCount(*, art_data: dict, github_data: dict) -> int:
    _today: str = datetime.today().strftime("%Y-%m-%d")
    _start_date: str = art_data["start_date"]
    _date_delta: int = _calDateDelta(today=_today, start_date=_start_date)

    _pixels_level: list = art_data["pixels_level"]
    _pixel_level: int = _calPixelLevel(
        date_delta=_date_delta, pixels_level=_pixels_level
    )

    print(f"\n{'Today:':<20} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    _date_count: Union[int, None] = github_data.get(_today, None)
    print(f"{'Commits in Github:':<20} {_date_count}\n")
    _commit_count: int = _calCommitCount(
        pixel_level=_pixel_level, date_count=_date_count
    )
    print(f"{'Need to commit more:':<20} {_commit_count}\n")

    return _commit_count
