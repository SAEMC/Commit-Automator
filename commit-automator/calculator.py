# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

from itertools import chain
from sys import exit
from typing import Union

from logger import logger


def _calculate_pixel_level(*, date_delta: int, pixels_level: list[list[int]]) -> int:
    _flattened_pixels_level: list[int] = list(chain(*pixels_level))
    _total_pixels: int = len(_flattened_pixels_level)
    _pixel_idx: int = date_delta % _total_pixels

    pixel_level: int = _flattened_pixels_level[_pixel_idx]

    return pixel_level


def _calculate_commit_count(*, pixel_level: int, date_count: Union[int, None]) -> int:
    _date_level: int
    _min_commit: int
    _date_count_is_none: bool = date_count is None

    try:
        if _date_count_is_none:
            raise ValueError("Cannot find commit count in Github now.. try later.")
    except ValueError as _e:
        logger.info(msg=_e)
        exit(1)

    _date_count_is_less_than_1: bool = date_count < 1
    _date_count_is_less_than_16: bool = date_count < 16
    _date_count_is_less_than_32: bool = date_count < 32
    _date_count_is_less_than_47: bool = date_count < 47

    if _date_count_is_less_than_1:
        _date_level = 0
    elif _date_count_is_less_than_16:
        _date_level = 1
    elif _date_count_is_less_than_32:
        _date_level = 2
    elif _date_count_is_less_than_47:
        _date_level = 3
    else:
        _date_level = 4

    _pixel_level_is_less_than_or_equal_to_date_level: bool = pixel_level <= _date_level

    try:
        if _pixel_level_is_less_than_or_equal_to_date_level:
            raise ValueError("Enough today.. nothing to commit.")
    except ValueError as _e:
        logger.info(msg=_e)
        exit(1)

    _pixel_level_is_1: bool = pixel_level == 1
    _pixel_level_is_2: bool = pixel_level == 2
    _pixel_level_is_3: bool = pixel_level == 3

    if _pixel_level_is_1:
        _min_commit = 1
    elif _pixel_level_is_2:
        _min_commit = 16
    elif _pixel_level_is_3:
        _min_commit = 32
    else:
        _min_commit = 47

    commit_count: int = _min_commit - date_count

    return commit_count


def get_commit_count(
    *,
    art_data: dict[str, Union[int, list[list[int]], str]],
    github_data: dict[str, int],
) -> int:
    _today: str = art_data["today"]
    _date_delta: int = art_data["date_delta"]

    _pixels_level: list[list[int]] = art_data["pixels_level"]
    _pixel_level: int = _calculate_pixel_level(
        date_delta=_date_delta, pixels_level=_pixels_level
    )

    _date_count: Union[int, None] = github_data.get(_today, None)

    logger.info(msg=f"{'Commits in Github:':<20} {_date_count}\n")

    commit_count: int = _calculate_commit_count(
        pixel_level=_pixel_level, date_count=_date_count
    )

    logger.info(msg=f"{'Need to commit more:':<20} {commit_count}\n")

    return commit_count
