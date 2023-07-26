# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

from typing import Union

from logger import log
from numpy import array, ndarray


def display_art(*, art_data: dict[str, Union[int, list[list[int]], str]]) -> None:
    _colors: list[str] = [
        ### 4-bit Colors
        "\033[97m",  # Bright White
        "\033[93m",  # Bright Yellow
        "\033[92m",  # Bright Green
        "\033[94m",  # Bright Blue
        "\033[95m",  # Bright Magenta
        "\033[0m",  # Nothing
    ]
    _user_name: str = art_data["user_name"]
    _art_name: str = art_data["art_name"]
    _duration: int = art_data["duration"]
    _pixels_level: list[list[int]] = art_data["pixels_level"]
    _pixels_level_t: ndarray = array(_pixels_level).T

    _lines: str = f""
    _lines += f" *{'-' * (_duration * 2 + 1)}*\n"

    for _pixels_level in _pixels_level_t:
        _line: str = f" |"

        for _pixel_level in _pixels_level:
            _line += f" {_colors[_pixel_level]}■{_colors[-1]}"

        _line += " |\n"
        _lines += _line

    _lines += f" *{'-' * (_duration * 2 + 1)}* {_art_name} by {_user_name}"

    log.info(msg=_lines)
