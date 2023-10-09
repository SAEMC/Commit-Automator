# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-08

from argparse import Action, ArgumentParser, Namespace
from datetime import datetime
from itertools import chain
from json import load
from os import path
from pathlib import Path
from typing import Any, Sequence, Union


class FileAction(Action):
    art_data: dict[str, Union[int, list[list[int]]], str]

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = None,
    ) -> None:
        _parent_directory: Path = Path(__file__).parents[1].absolute()
        _art_path: Path = _parent_directory / values

        ### Check extension is '.json'
        _extension: str = path.splitext(p=values)[-1]
        _extension_is_not_json: bool = _extension != ".json"

        if _extension_is_not_json:
            parser.error(
                message=f"Invalid extension of file: {values}\n"
                "Extension of the art file must be '.json'!"
            )

        ### Check file exists
        _art_path_does_not_exist: bool = not path.exists(path=_art_path)

        if _art_path_does_not_exist:
            parser.error(
                message=f"Invalid path of file: {_art_path}\n"
                "No such file or directory!"
            )

        ### Check keys in art file are vaild
        _vaild_keys: set[str] = {
            "user_name",
            "art_name",
            "start_date",
            "duration",
            "pixels_level",
        }

        with open(file=_art_path) as _file:
            _art_dict: dict[str, Union[int, list[list[int]], str]] = load(fp=_file)

        _invalid_keys_exist: str = f""
        _invalid_count: int = 0

        for _key in list(_art_dict.keys()):
            _key_is_not_in_vaild_keys: bool = _key not in _vaild_keys

            if _key_is_not_in_vaild_keys:
                _invalid_keys_exist += f"'{_key}', "
                _invalid_count += 1

        if _invalid_keys_exist:
            parser.error(
                message=f"Invalid key{'s' if _invalid_count > 1 else ''} of '{values}': {_invalid_keys_exist[:-2]}\n"
                f"The keys must be {_vaild_keys}!"
            )

        ### Check 'start_date' is Sunday
        _start_date: str = _art_dict["start_date"]
        _start_day: str = datetime.strptime(_start_date, "%Y-%m-%d").strftime("%a")
        _start_day_is_not_sunday: bool = _start_day != "Sun"

        if _start_day_is_not_sunday:
            parser.error(
                message=f"Invalid day of 'start_date': {_start_day}\n"
                "'start_date' must start from Sunday!"
            )

        ### Check 'duration' and 'pixels_level' are same
        _duration: int = _art_dict["duration"]
        _pixels_level: list[list[int]] = _art_dict["pixels_level"]
        _duration_is_not_same_with_length_of_pixels_level: bool = _duration != len(
            _pixels_level
        )

        if _duration_is_not_same_with_length_of_pixels_level:
            parser.error(
                message=f"Invalid value of 'duration': {_duration}\n"
                "'duration' must be same with length of 'pixels_level'!"
            )

        ### Check 'pixels_level' is valid
        _pixels_level: list[list[int]] = _art_dict["pixels_level"]
        _flattened_pixels_level: list[int] = list(chain(*_pixels_level))
        _invalid_pixels_level_exists: set[int] = {
            _level for _level in _flattened_pixels_level if not (0 <= _level <= 4)
        }

        if _invalid_pixels_level_exists:
            parser.error(
                message=f"Invalid value of 'pixels_level': {_invalid_pixels_level_exists}\n"
                "The value of 'pixels_level' must be '0' ~ '4'!"
            )

        ### Check 'start_date' is valid
        _today: str = datetime.today().strftime("%Y-%m-%d")
        _today_for_calculation: datetime = datetime.strptime(_today, "%Y-%m-%d")
        _start_date_for_calculation: datetime = datetime.strptime(
            _start_date, "%Y-%m-%d"
        )
        _date_delta: int = (_today_for_calculation - _start_date_for_calculation).days
        _date_delta_is_less_than_0: bool = _date_delta < 0

        if _date_delta_is_less_than_0:
            parser.error(
                message=f"Invalid value of 'start_date': {_start_date_for_calculation:%Y-%m-%d}\n"
                f"'start_date' must be earlier than or equal to today: {_today_for_calculation:%Y-%m-%d}!"
            )

        _art_dict["today"] = _today
        _art_dict["date_delta"] = _date_delta

        ### Set class attributes
        setattr(namespace, self.dest, values)
        FileAction.art_data = _art_dict
