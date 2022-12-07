# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-08

import argparse
import json
import os
from pathlib import Path
from typing import Any, Sequence, Union


class FileAction(argparse.Action):
    art_dict: dict

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = None,
    ) -> None:
        _ext: str = os.path.splitext(p=values)[-1]

        if _ext != ".json":
            parser.error(f"Extension of the art file must be '.json'!")

        _parent_dir: Path = Path(__file__).parents[1].absolute()
        _art_path: Path = _parent_dir / values

        if not os.path.exists(path=_art_path):
            parser.error(f"No such file or directory: {_art_path}")

        _right_keys: list = [
            "user_name",
            "art_name",
            "start_date",
            "duration",
            "pixels_level",
        ]

        with open(file=_art_path) as _file:
            _art_dict: dict = json.load(fp=_file)

        _wrong_keys: str = f""
        _wrong_count: int = 0
        _verb: str = "is"

        for _key in list(_art_dict.keys()):
            if _key not in _right_keys:
                _wrong_keys += f"'{_key}', "
                _wrong_count += 1

        if _wrong_count > 1:
            _verb = "are"

        if _wrong_keys:
            _wrong_keys = _wrong_keys[:-2]
            parser.error(f"{_wrong_keys} {_verb} wrong in {values}!")

        setattr(namespace, self.dest, values)
        FileAction.art_dict = _art_dict
