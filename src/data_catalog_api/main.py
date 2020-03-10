from fastapi import FastAPI
import store

app = FastAPI()

@app.get("/")
async def root():
    response =  await store.get_count()
    return response

@app.get("/count")
async def get_count():
    response = await store.get_count()
    return response

@app.get("/nodes/{node_id}")
async def get_node_by_id(node_id: str):
    response = await store.get_node_by_id(node_id)
    return response

@app.get("/nodes/{label}/{node_id}")
async def get_node_by_label_and_id(label: str, node_id: str):
    response = await store.get_node_by_label_id(label, node_id)
    return response

@app.put("/property/{node_id}/{prop_key}/{prop_val}")
async def put_node_property(node_id: str, prop_key: str, prop_val:str):
    response = await store.add_property_to_node(node_id, prop_key, prop_val)
    return response

@app.put("/node/{label}/{id}/{content}")
async def put_node(label: str, id: str, content: str):
    response = await store.upsert_node(label, id, content)
    return response