# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-08

from datetime import datetime
from pathlib import Path
from typing import Any, Sequence, Union
import argparse
import itertools
import json
import os


class FileAction(argparse.Action):
    art_data: dict

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = None,
    ) -> None:
        _parent_dir: Path = Path(__file__).parents[1].absolute()
        _art_path: Path = _parent_dir / values

        ### Check extension is '.json'
        _ext: str = os.path.splitext(p=values)[-1]

        if _ext != ".json":
            parser.error(
                message=f"Invalid extension of file: {values}\n"
                "Extension of the art file must be '.json'!"
            )

        ### Check file exists
        if not os.path.exists(path=_art_path):
            parser.error(
                message=f"Invalid path of file: {_art_path}\n"
                "No such file or directory!"
            )

        ### Check keys in art file are vaild
        _vaild_keys: set = {
            "user_name",
            "art_name",
            "start_date",
            "duration",
            "pixels_level",
        }

        with open(file=_art_path) as _file:
            _art_dict: dict = json.load(fp=_file)

        _invalid_keys: str = f""
        _invalid_count: int = 0

        for _key in list(_art_dict.keys()):
            if _key not in _vaild_keys:
                _invalid_keys += f"'{_key}', "
                _invalid_count += 1

        if _invalid_keys:
            parser.error(
                message=f"Invalid key{'s' if _invalid_count > 1 else ''} of '{values}': {_invalid_keys[:-2]}\n"
                f"The keys must be {_vaild_keys}!"
            )

        ### Check 'start_date' is Sunday
        _start_date: str = _art_dict["start_date"]
        _start_day: str = datetime.strptime(_start_date, "%Y-%m-%d").strftime("%a")

        if _start_day != "Sun":
            parser.error(
                message=f"Invalid day of 'start_date': {_start_day}\n"
                "'start_date' must start from Sunday!"
            )

        ### Check 'duration' and 'pixels_level' are same
        _duration: int = _art_dict["duration"]
        _pixels_level: list = _art_dict["pixels_level"]

        if _duration != len(_pixels_level):
            parser.error(
                message=f"Invalid value of 'duration': {_duration}\n"
                "'duration' must be same with length of 'pixels_level'!"
            )

        ### Check 'pixels_level' in art file is valid
        _pixels_level: list = _art_dict["pixels_level"]
        _flatten_pixels_level: list = list(itertools.chain(*_pixels_level))

        _invalid_pixels_level: set = {
            _level for _level in _flatten_pixels_level if _level < 0 or _level > 4
        }

        if _invalid_pixels_level:
            parser.error(
                message=f"Invalid value of 'pixels_level': {_invalid_pixels_level}\n"
                "The value of 'pixels_level' must be '0' ~ '4'!"
            )

        setattr(namespace, self.dest, values)
        FileAction.art_data = _art_dict
