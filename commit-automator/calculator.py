# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import sys
from datetime import datetime
from typing import Union

from logger import log


def _calDateDelta(*, today: str, start_date: str) -> int:
    _today: datetime = datetime.strptime(today, "%Y-%m-%d")
    _start_date: datetime = datetime.strptime(start_date, "%Y-%m-%d")
    _date_delta: int = (_today - _start_date).days

    try:
        if _date_delta < 0:
            raise ValueError(f"'start_date' must be earlier than or equal to today!")
    except ValueError as e:
        log.error(msg=e)
        sys.exit(1)

    return _date_delta


def _calPixelLevel(*, date_delta: int, pixels_level: list) -> int:
    _flatten_pixels_level: list = list(itertools.chain(*pixels_level))
    _total_pixels: int = len(_flatten_pixels_level)
    _pixel_idx: int = date_delta % _total_pixels
    _pixel_level: int = _flatten_pixels_level[_pixel_idx]

    return _pixel_level


def _calCommitCount(*, pixel_level: int, date_count: Union[int, None]) -> int:
    _date_level: int
    _min_commit: int

    try:
        if date_count is None:
            raise ValueError(f"Cannot find commit count in Github now.. try later.")
    except ValueError as e:
        log.info(msg=e)
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
            raise ValueError(f"Enough today.. nothing to commit.")
    except ValueError as e:
        log.info(msg=e)
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

    _date_count: Union[int, None] = github_data.get(_today, None)
    log.info(msg=f"{'Commits in Github:':<20} {_date_count}\n")
    _commit_count: int = _calCommitCount(
        pixel_level=_pixel_level, date_count=_date_count
    )
    log.info(msg=f"{'Need to commit more:':<20} {_commit_count}\n")

    return _commit_count
