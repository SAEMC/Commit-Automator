# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

from itertools import chain
from sys import exit
from typing import Union

from httpx import Client, Response
from logger import log


def get_github_data(*, user_name: str, access_token: str) -> dict[str, int]:
    with Client() as _client:
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

        _response: Response = _client.post(
            url=_url, headers=_headers, json={"query": _body}
        )

    try:
        if _response.status_code == 200:
            _response_json: dict[
                str,
                dict[
                    str,
                    dict[
                        str,
                        dict[
                            str,
                            dict[
                                str,
                                Union[
                                    int,
                                    list[dict[str, list[dict[str, Union[int, str]]]]],
                                ],
                            ],
                        ],
                    ],
                ],
            ] = _response.json()
            _data: dict[
                str,
                dict[
                    str,
                    dict[
                        str,
                        dict[
                            str,
                            Union[
                                int, list[dict[str, list[dict[str, Union[int, str]]]]]
                            ],
                        ],
                    ],
                ],
            ] = _response_json["data"]
            _user: dict[
                str,
                dict[
                    str,
                    dict[
                        str,
                        Union[int, list[dict[str, list[dict[str, Union[int, str]]]]]],
                    ],
                ],
            ] = _data["user"]
            _contributions_collection: dict[
                str,
                dict[
                    str, Union[int, list[dict[str, list[dict[str, Union[int, str]]]]]]
                ],
            ] = _user["contributionsCollection"]
            _contribution_calendar: dict[
                str, Union[int, list[dict[str, list[dict[str, Union[int, str]]]]]]
            ] = _contributions_collection["contributionCalendar"]
            _weeks: list[
                dict[str, list[dict[str, Union[int, str]]]]
            ] = _contribution_calendar["weeks"]

            _contribution_days: list[list[dict[str, Union[int, str]]]] = [
                _values for _week in _weeks for _values in _week.values()
            ]
            _flattened_contribution_days: list[dict[str, Union[int, str]]] = list(
                chain(*_contribution_days)
            )

            github_data: dict[str, int] = {
                _element.get("date"): int(_element.get("contributionCount"))
                for _element in _flattened_contribution_days
                if _element.get("date")
            }

            return github_data
        else:
            raise ValueError(f"'response' is {_response.text}!")
    except ValueError as _e:
        log.error(msg=_e)
        exit(1)
