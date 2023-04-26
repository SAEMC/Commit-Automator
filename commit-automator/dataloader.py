# -*- coding: utf-8 -*-
# Author: SAEMC
# Date: 2022-12-07

import itertools
import sys

import httpx
from logger import log


def get_github_data(*, user_name: str, access_token: str) -> dict:
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
        log.error(msg=e)
        sys.exit(1)
