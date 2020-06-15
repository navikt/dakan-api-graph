import json
import os

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
    logger.log.info("test1")
    redirect_uri = f'{os.environ["INGRESS"]}/auth'
    response = await oauth.azure.authorize_redirect(request, redirect_uri)
    response.set_cookie(key="Redirect-url", value=redirect_url)
    return response


@router.get("/auth")
async def auth_via_azure(request: Request):
    response = RedirectResponse(request.cookies.get("Redirect-url"))
    response.delete_cookie(key="Redirect-url")
    token = await oauth.azure.authorize_access_token(request)
    user = await oauth.azure.parse_id_token(request, token)
    logger.log.info(f"User {user['name']} logged in")
    response.delete_cookie(key="ClientName")
    response.set_cookie(key="ClientName", value=user.get("name"))
    response.delete_cookie(key="ClientToken")
    response.set_cookie(key="ClientToken", value=token.get("access_token"))
    return response
