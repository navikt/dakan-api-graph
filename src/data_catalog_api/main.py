from fastapi import FastAPI
from data_catalog_api.routers import nodes, edges, health

app = FastAPI()

app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(health.router)
