from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class CreateItemRequest(BaseModel):
    name: str
    description: str

class CreateItemResponse(BaseModel):
    name: str
    
class ErrorResponse(BaseModel):
    detail: str

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items", status_code=201, responses={
                201: {"model": CreateItemResponse, "description": "Create item success"}, 
                400: {"model": ErrorResponse, "description": "Item name can not be test"}, 
                })
def create_item(data: CreateItemRequest):
    print(data)
    data = data.model_dump()
    print(data)
    if data['name'] == "test":
        raise HTTPException(status_code=400, detail="Item name can not be test") 
    return CreateItemResponse(**data)
