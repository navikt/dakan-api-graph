import json
import os
import requests
from starlette import status
from starlette.requests import Request
from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth
from starlette.responses import JSONResponse, RedirectResponse
from data_catalog_api.utils.logger import Logger


logger = Logger()

oauth = OAuth()

router = APIRouter()

oauth.register(
    'azure',
    client_id=os.environ["client_id"],
    client_secret=os.environ["client_secret"],
    server_metadata_url='https://login.microsoftonline.com/62366534-1ec3-4962-8869-9b5535279d0b/v2.0/.well-known/'
                        'openid-configuration',
    client_kwargs={'scope': 'openid email profile https://graph.microsoft.com/.default'}
)


@router.get("/login")
async def login_via_azure(request: Request, redirect_url: str):
    redirect_uri = f'{os.environ["INGRESS"]}/auth'
    response = await oauth.azure.authorize_redirect(request, redirect_uri)
    response.set_cookie(key="Redirect-url", value=redirect_url)
    return response


@router.get("/auth")
async def auth_via_azure(request: Request):
    response = RedirectResponse(request.cookies.get("Redirect-url"))
    response.delete_cookie(key="Redirect-url")
    token = await oauth.azure.authorize_access_token(request)

    headers = {'Authorization': f'Bearer {token.get("access_token")}'}
    query = 'onPremisesSamAccountName,givenName,mail,surname'
    r = requests.get(f'https://graph.microsoft.com/v1.0/me?$select={query}', headers=headers)
    user = r.json()

    client_user = {
        "userId": user["onPremisesSamAccountName"],
        "givenName": user["givenName"],
        "surname": user["surname"],
        "initial": f"{user['givenName'][0]}{user['surname'][0]}",
        "email": user["mail"]
    }

    # user = await oauth.azure.parse_id_token(request, token)
    response.delete_cookie(key="ClientUser")
    response.set_cookie(key="ClientUser", value=json.dumps(client_user), max_age=3600, expires=3600)
    response.delete_cookie(key="ClientToken")
    response.set_cookie(key="ClientToken", value=token.get("access_token"), max_age=3600, expires=3600)
    return response


@router.get("/logout")
async def logout_via_azure(request: Request, redirect_url: str):
    post_logout_url = f"?post_logout_redirect_uri={redirect_url}"
    logout_url = oauth.azure.server_metadata.get('end_session_endpoint', None)
    request.session.pop('user', None)
    if logout_url:
        response = RedirectResponse(url=logout_url + post_logout_url)
        response.delete_cookie(key="ClientToken")
        response.delete_cookie(key="ClientName")
        return response
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"Error": "Unable to logout, something went wrong"})
