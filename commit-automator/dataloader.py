# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import json
import sys
from datetime import datetime
from pathlib import Path

import httpx


def getGithubData(*, user_name: str, access_token: str) -> dict:
    with httpx.Client() as _client:
        _url = "https://api.github.com/graphql"
        _headers = {
            "Content-Type": "application/graphql",
            "Authorization": "Bearer " + access_token,
        }
        _body = f"""
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

        _response = _client.post(url=_url, headers=_headers, json={"query": _body})

    try:
        if _response.status_code == 200:
            _result = _response.json()["data"]["user"]["contributionsCollection"][
                "contributionCalendar"
            ]["weeks"]
            _contribution_days = [
                _values for _element in _result for _values in _element.values()
            ]
            _contribution_days = list(itertools.chain(*_contribution_days))

            _github_data = {
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


def getArtData(*, art_path: Path) -> dict:
    with open(art_path) as _file:
        _art_data = json.load(_file)

    _start_date = datetime.strptime(_art_data["start_date"], "%Y-%m-%d").strftime("%a")

    try:
        if _start_date != "Sun":
            raise ValueError("'start_date' must start from Sunday!")
    except ValueError as e:
        print(e)
        sys.exit(1)

    try:
        if _art_data["duration"] != len(_art_data["pixels_level"]):
            raise ValueError("'duration' must be same with 'pixels_level'!")
    except ValueError as e:
        print(e)
        sys.exit(1)

    return _art_data
