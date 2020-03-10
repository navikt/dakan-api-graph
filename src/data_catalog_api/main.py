from data_catalog_api import store
from fastapi import FastAPI
from data_catalog_api.routers import nodes, edges

app = FastAPI()


@app.get("/")
async def root():
    response = await store.get_count()
    return response


app.include_router(nodes.router)
app.include_router(edges.router)
