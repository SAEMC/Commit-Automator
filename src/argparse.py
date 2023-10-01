# -*- coding: utf-8 -*-
# Init Author: SAEMC
# Date: 2023-10-02

from argparse import Namespace


class _BaseArgParser:
    def _set_attributes(self, *, namespace: Namespace) -> None:
        _args: dict[str, str] = vars(namespace)

        for _key, _value in _args.items():
            setattr(self, _key, _value)


class AppArgParser(_BaseArgParser):
    def __init__(self, *, namespace: Namespace) -> None:
        self.execute: str
        self.is_save_log: str

        self._set_attributes(namespace=namespace)
