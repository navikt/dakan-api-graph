import os
from typing import Mapping
from data_catalog_api.exceptions.exceptions import EnvironmentVariableNotSet


def is_authorized(headers: Mapping):
    try:
        token = headers["Authorization"].split(' ')[-1]
    except KeyError:
        return False
    else:
        return _verify_token(token)


def _verify_token(token: str):
    try:
        expected_token = os.environ["API_TOKEN"]
    except KeyError as env:
        raise EnvironmentVariableNotSet(env)
    else:
        return token == expected_token
