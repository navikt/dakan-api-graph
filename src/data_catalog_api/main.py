from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from data_catalog_api.routers import nodes, edges, health, azure_ad
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(docs_url=None, redoc_url=None, swagger_static={"favicon": "/static/favicon.png"})

app.mount("/static", StaticFiles(directory="src/data_catalog_api/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we need this to save temporary code & state in session
app.add_middleware(SessionMiddleware, secret_key="random-key-here-123456")


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(health.router)
app.include_router(azure_ad.router)

