from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from data_catalog_api.routers import nodes, edges, health

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(health.router)
