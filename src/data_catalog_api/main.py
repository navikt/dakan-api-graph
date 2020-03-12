from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from data_catalog_api.routers import nodes, edges, health

app = FastAPI()

app.mount("src/data_catalog_api/static", StaticFiles(directory="static"), name="static")

app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(health.router)
