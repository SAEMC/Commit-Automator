# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import sys
from datetime import datetime

import httpx


def getGithubData(*, user_name: str, access_token: str) -> dict:
    with httpx.Client() as _client:
        _url: str = "https://api.github.com/graphql"
        _headers: dict = {
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
            _result: list = _response.json()["data"]["user"]["contributionsCollection"][
                "contributionCalendar"
            ]["weeks"]
            _contribution_days: list = [
                _values for _element in _result for _values in _element.values()
            ]
            _contribution_days: list = list(itertools.chain(*_contribution_days))
            _github_data: dict = {
                _element.get("date"): int(_element.get("contributionCount"))
                for _element in _contribution_days
                if _element.get("date")
            }

            return _github_data
        else:
            raise ValueError(f"'response' is {_response.text}!")
    except ValueError as e:
        print(e)
        sys.exit(1)


def getArtData(*, art_dict: dict) -> dict:
    _start_date: str = art_dict["start_date"]
    _start_day: str = datetime.strptime(_start_date, "%Y-%m-%d").strftime("%a")

    try:
        if _start_day != "Sun":
            raise ValueError("'start_date' must start from Sunday!")
    except ValueError as e:
        print(e)
        sys.exit(1)

    _duration: int = art_dict["duration"]
    _pixels_level: list = art_dict["pixels_level"]

    try:
        if _duration != len(_pixels_level):
            raise ValueError("'duration' must be same with 'pixels_level'!")
    except ValueError as e:
        print(e)
        sys.exit(1)

    _art_data: dict = art_dict

    return _art_data
