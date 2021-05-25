import os
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from dakan_api_graph.routers import nodes, edges, health, azure_ad, metrics
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
subapi = FastAPI(docs_url='/docs', swagger_static={"favicon": "/static/favicon.png"},
                 openapi_prefix="/cosmosdb", default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory="src/data_catalog_api/static"), name="static")
app.mount("/cosmosdb", subapi)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we need this to save temporary code & state in session
app.add_middleware(SessionMiddleware, secret_key=os.environ["session_secret_key"])


@subapi.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=subapi.openapi_url,
        title=subapi.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


subapi.include_router(metrics.router)
subapi.include_router(nodes.router)
subapi.include_router(edges.router)
subapi.include_router(health.router)
subapi.include_router(azure_ad.router)
