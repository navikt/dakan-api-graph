import os
import requests
from data_catalog_api.utils.logger import Logger
from typing import Mapping
from data_catalog_api.exceptions.exceptions import EnvironmentVariableNotSet
from starlette.requests import Request

logger = Logger()


def is_authorized(request: Request):
    if request.headers.get("Authorization"):
        return _verify_token(request.headers["Authorization"].split(' ')[-1])
    else:
        return _verify_user(request)


def _verify_token(token: str):
    try:
        expected_token = os.environ["API_TOKEN"]
    except KeyError as env:
        raise EnvironmentVariableNotSet(env)
    else:
        return token == expected_token


def _verify_user(request: Request):
    logger.log.info(request.session)
    # try:
    #     valid_groups = os.environ["VALID_AAD_GROUPS"]
    # except KeyError as env:
    #     raise EnvironmentVariableNotSet(env)
    # else:
    #     return False
        #return _is_user_authorized(client_info, valid_groups)


def _is_user_authorized(client_info: Mapping, valid_groups: str):
    for group_id in client_info["groups"]:
        if group_id in valid_groups.split(","):
            return True
    return False


def _get_user_info(token):
    headers = {'Authorization': f'Bearer {token}'}
    #query = 'onPremisesSamAccountName,displayName,givenName,mail,officeLocation,surname,userPrincipalName,id,jobTitle' \
    #        ',memberOf'
    query = 'id'
    #r = requests.get(f'https://graph.microsoft.com/v1.0/me?$select={query}', headers=headers)
    r = requests.get(f'https://graph.microsoft.com/v1.0/me/memberOf?$select={query}', headers=headers)
    return r.json()
