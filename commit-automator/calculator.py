# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
from datetime import datetime
from typing import Union


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
