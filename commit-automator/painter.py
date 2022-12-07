# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import numpy as np


def displayArt(*, art_data: dict) -> None:
    _colors: list = [
        # The way how to set colors:
        # \033[38;2;<r>;<g>;<b>;m] - foreground color
        # \033[48;2;<r>;<g>;<b>;m] - background color
        # \033[38;2;<r>;<g>;<b>;48;2;<r>;<g>;<b>m] - fore/background color
        "\033[38;2;234;237;240m",
        "\033[38;2;198;224;180m",
        "\033[38;2;168;207;142m",
        "\033[38;2;55;86;35m",
        "\033[38;2;64;64;64m",
        "\033[0m",
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
