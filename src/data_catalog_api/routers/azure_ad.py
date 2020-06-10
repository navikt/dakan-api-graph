from starlette.requests import Request
from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from data_catalog_api.utils.logger import Logger
import os

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
async def login_via_azure(request: Request):
    logger.log.info(request.headers.get("Origin"))
    redirect_uri = f'{os.environ["INGRESS"]}/auth'
    return await oauth.azure.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth_via_azure(request: Request):
    token = await oauth.azure.authorize_access_token(request)
    user = await oauth.azure.parse_id_token(request, token)
    return dict(user)
