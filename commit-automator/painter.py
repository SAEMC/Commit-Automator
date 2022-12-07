# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import numpy as np


def displayArt(*, art_data: dict) -> None:
    _colors: list = [
        # 4-bit Colors
        "\033[97m",  # Bright White
        "\033[93m",  # Bright Yellow
        "\033[92m",  # Bright Green
        "\033[94m",  # Bright Blue
        "\033[95m",  # Bright Magenta
        "\033[0m",  # Nothing
    ]
    _art_name: str = art_data["art_name"]
    _start_date: str = art_data["start_date"]
    _duration: int = art_data["duration"]
    _pixels_level: list = art_data["pixels_level"]
    _pixels_level_t: np.ndarray = np.array(_pixels_level).T

    print(
        f"Name of art: {_art_name}\n"
        f"Start date: {_start_date}\n"
        f"Duration: {_duration}\n"
    )

    for _pixels_level in _pixels_level_t:
        line: str = f""

        for _pixel_level in _pixels_level:
            line += f" {_colors[_pixel_level]}■{_colors[-1]}"

        print(line)

    print("")
