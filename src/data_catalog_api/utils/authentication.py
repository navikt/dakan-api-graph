import os
import requests
from data_catalog_api.utils.logger import Logger
from typing import Mapping
from data_catalog_api.exceptions.exceptions import EnvironmentVariableNotSet

logger = Logger()


def is_authorized(headers: Mapping):
    if headers.get("Authorization"):
        return _verify_token(headers["Authorization"].split(' ')[-1])
    else:
        return _verify_user(headers.get("JWT-Token"))


def _verify_token(token: str):
    try:
        expected_token = os.environ["API_TOKEN"]
    except KeyError as env:
        raise EnvironmentVariableNotSet(env)
    else:
        return token == expected_token


def _verify_user(jwt_token: str):
    try:
        user_groups = _get_user_info(jwt_token)
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
        logger.log.error(err)
        return False

    try:
        valid_groups = os.environ["VALID_AAD_GROUPS"]
    except KeyError as env:
        raise EnvironmentVariableNotSet(env)
    else:
        return _is_user_authorized(user_groups, valid_groups)


def _is_user_authorized(user_groups: Mapping, valid_groups: str):
    for group_id in user_groups:
        if group_id["id"] in valid_groups.split(","):
            return True
    return False


def _get_user_info(token):
    """
    example of query string:
        query = 'onPremisesSamAccountName,displayName,givenName,mail,officeLocation,surname,userPrincipalName,id,jobTitle'
    """
    headers = {'Authorization': f'Bearer {token}'}
    query = 'id'
    r = requests.get(f'https://graph.microsoft.com/v1.0/me/memberOf?$select={query}', headers=headers)
    r.raise_for_status()
    return r.json()["value"]
