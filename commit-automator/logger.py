# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-09

import logging
from pathlib import Path

log: logging.Logger = logging.getLogger(name="automator")
log.setLevel(level=logging.INFO)

_formatter: logging.Formatter = logging.Formatter(
    fmt="***** {levelname:<8} - {asctime} *****\n\n{message}\n",
    datefmt="%Y/%m/%d %H:%M:%S",
    style="{",
)

_stream_handler: logging.StreamHandler = logging.StreamHandler()
_stream_handler.setLevel(level=logging.INFO)
_stream_handler.setFormatter(fmt=_formatter)

log.addHandler(hdlr=_stream_handler)


def save_log() -> None:
    _parent_dir: Path = Path(__file__).parents[1].absolute()
    _log_path: Path = _parent_dir / "automator.log"

    _file_handler: logging.FileHandler = logging.FileHandler(filename=_log_path)
    _file_handler.setLevel(level=logging.INFO)
    _file_handler.setFormatter(fmt=_formatter)

    log.addHandler(hdlr=_file_handler)
