from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from data_catalog_api.routers import nodes, edges, health
from fastapi.openapi.docs import get_swagger_ui_html
from starlette_exporter import PrometheusMiddleware, handle_metrics

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.mount("/static", StaticFiles(directory="src/data_catalog_api/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(health.router)
