# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import numpy as np


_colors = [
    "\033[38;2;234;237;240m",
    "\033[38;2;154;233;168m",
    "\033[38;2;65;195;99m",
    "\033[38;2;49;161;78m",
    "\033[38;2;32;109;56m",
    "\033[0m",
]


def displayArt(*, art_data: dict) -> None:
    _art_name = art_data["art_name"]
    _start_date = art_data["start_date"]
    _duration = art_data["duration"]
    _pixels_level = art_data["pixels_level"]
    _pixels_level_t = np.array(_pixels_level).T

    print(
        f"Name of art: {_art_name}\n"
        f"Start date: {_start_date}\n"
        f"Duration: {_duration}\n"
    )

    for _pixels_level in _pixels_level_t:
        line = f""

        for _pixel_level in _pixels_level:
            line += f" {_colors[_pixel_level]}■{_colors[-1]}"

        print(line)

    print("")
