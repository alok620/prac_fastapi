from typing import List, Dict, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

from transformers import pipeline, set_seed

from .imps import imp

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class Prediction(BaseModel):
        instances: List[Dict] = []

app = FastAPI()


@app.get("/")
def read_root():
    yay = imp.getYay()
    return {"Hello": yay}

@app.post("/prediction")
async def getPred(pred: Prediction):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(103)
    res = generator(pred.instances[0]["instance_key_1"], max_length=30, num_return_sequences=5)
    return {"predictions": res}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/health", status_code=200)
async def health_check():
    return {"Everything": "OK!"}

