from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Items(BaseModel):
    text:str 
    is_done:bool = False

items = []

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item:Items):
    items.append(item)
    return items

@app.get("/items", response_model=list[Items])
def list_items(limit:int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Items)
def get_item(item_id:int)->Items:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id < len(items):
        deleted = items.pop(item_id)
        return deleted
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Items):
    if item_id < len(items):
        items[item_id] = updated_item
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")