# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import sys
from typing import Union

from logger import log


def _cal_pixel_level(*, date_delta: int, pixels_level: list) -> int:
    _flatten_pixels_level: list = list(itertools.chain(*pixels_level))
    _total_pixels: int = len(_flatten_pixels_level)
    _pixel_idx: int = date_delta % _total_pixels
    _pixel_level: int = _flatten_pixels_level[_pixel_idx]

    return _pixel_level


def _cal_commit_count(*, pixel_level: int, date_count: Union[int, None]) -> int:
    _date_level: int
    _min_commit: int

    try:
        if date_count is None:
            raise ValueError("Cannot find commit count in Github now.. try later.")
    except ValueError as e:
        log.info(msg=e)
        sys.exit(1)

    if date_count < 1:
        _date_level = 0
    elif date_count < 16:
        _date_level = 1
    elif date_count < 32:
        _date_level = 2
    elif date_count < 47:
        _date_level = 3
    else:
        _date_level = 4

    try:
        if pixel_level <= _date_level:
            raise ValueError("Enough today.. nothing to commit.")
    except ValueError as e:
        log.info(msg=e)
        sys.exit(1)

    if pixel_level == 1:
        _min_commit = 1
    elif pixel_level == 2:
        _min_commit = 16
    elif pixel_level == 3:
        _min_commit = 32
    else:
        _min_commit = 47

    _commit_count: int = _min_commit - date_count

    return _commit_count


def get_commit_count(
    *,
    art_data: dict[str, Union[str, int, list[list[int]]]],
    github_data: dict[str, int],
) -> int:
    _today: str = art_data["today"]
    _date_delta: int = art_data["date_delta"]

    _pixels_level: list = art_data["pixels_level"]
    _pixel_level: int = _cal_pixel_level(
        date_delta=_date_delta, pixels_level=_pixels_level
    )

    _date_count: Union[int, None] = github_data.get(_today, None)
    log.info(msg=f"{'Commits in Github:':<20} {_date_count}\n")
    _commit_count: int = _cal_commit_count(
        pixel_level=_pixel_level, date_count=_date_count
    )
    log.info(msg=f"{'Need to commit more:':<20} {_commit_count}\n")

    return _commit_count
