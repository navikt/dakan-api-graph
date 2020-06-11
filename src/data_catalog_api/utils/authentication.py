import os
from typing import Mapping
from data_catalog_api.exceptions.exceptions import EnvironmentVariableNotSet


def is_authorized(headers: Mapping):
    if headers.get("Authorization"):
        return _verify_token(headers["Authorization"].split(' ')[-1])
    elif headers.get("Client-Info"):
        return _verify_user(headers["Client-Info"])
    else:
        return False


def _verify_token(token: str):
    try:
        expected_token = os.environ["API_TOKEN"]
    except KeyError as env:
        raise EnvironmentVariableNotSet(env)
    else:
        return token == expected_token


def _verify_user(client_info: Mapping):
    try:
        valid_groups = os.environ["VALID_AAD_GROUPS"]
    except KeyError as env:
        raise EnvironmentVariableNotSet(env)
    else:
        return _is_user_authorized(client_info, valid_groups)


def _is_user_authorized(client_info: Mapping, valid_groups: str):
    for group_id in client_info["groups"]:
        if group_id in valid_groups.split(","):
            return True
    return False
