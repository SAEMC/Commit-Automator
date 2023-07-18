# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import sys
from typing import Union

import httpx
from logger import log


def get_github_data(*, user_name: str, access_token: str) -> dict[str, int]:
    with httpx.Client() as _client:
        _url: str = "https://api.github.com/graphql"
        _headers: dict[str, str] = {
            "Content-Type": "application/graphql",
            "Authorization": "Bearer " + access_token,
        }
        _body: str = f"""
        query {{
            user(login: "{user_name}") {{
                contributionsCollection {{
                    contributionCalendar {{
                        totalContributions weeks {{
                            contributionDays {{
                                contributionCount date
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """

        _response: httpx.Response = _client.post(
            url=_url, headers=_headers, json={"query": _body}
        )

    try:
        if _response.status_code == 200:
            _result: list[
                dict[str, list[dict[str, Union[int, str]]]]
            ] = _response.json()["data"]["user"]["contributionsCollection"][
                "contributionCalendar"
            ][
                "weeks"
            ]
            _contribution_days: list[list[dict[str, Union[int, str]]]] = [
                _values for _element in _result for _values in _element.values()
            ]
            _contribution_days: list[dict[str, Union[int, str]]] = list(
                itertools.chain(*_contribution_days)
            )

            github_data: dict[str, int] = {
                _element.get("date"): int(_element.get("contributionCount"))
                for _element in _contribution_days
                if _element.get("date")
            }

            return github_data
        else:
            raise ValueError(f"'response' is {_response.text}!")
    except ValueError as _e:
        log.error(msg=_e)
        sys.exit(1)
