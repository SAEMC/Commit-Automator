# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-09

from logging import INFO, FileHandler, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path

logger: Logger = getLogger(name="automator")
logger.setLevel(level=INFO)

_formatter: Formatter = Formatter(
    fmt="***** {levelname:<8} - {asctime} *****\n\n{message}\n",
    datefmt="%Y/%m/%d %H:%M:%S",
    style="{",
)

_stream_handler: StreamHandler = StreamHandler()
_stream_handler.setLevel(level=INFO)
_stream_handler.setFormatter(fmt=_formatter)

logger.addHandler(hdlr=_stream_handler)


def save_log() -> None:
    _parent_dir: Path = Path(__file__).parents[1].absolute()
    _log_path: Path = _parent_dir / "automator.log"

    _file_handler: FileHandler = FileHandler(filename=_log_path)
    _file_handler.setLevel(level=INFO)
    _file_handler.setFormatter(fmt=_formatter)

    logger.addHandler(hdlr=_file_handler)
