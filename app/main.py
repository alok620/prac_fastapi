from typing import List, Dict, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

from transformers import pipeline, set_seed

from fastapi import FastAPI, status, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .imps import imp

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class Prediction(BaseModel):
        instances: List[Dict] = []

app = FastAPI()

templates = Jinja2Templates(directory='app/templates')

app.mount('/static/', StaticFiles(directory='app/static'), name='static')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('home.html',
            {'request': request})

"""
@app.post("/prediction")
async def getPred(pred: Prediction):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(103)
    res = generator(pred.instances[0]["instance_key_1"], max_length=30, num_return_sequences=5)
    return {"predictions": res}
"""
@app.post("/submit")
async def submit(request: Request, taskname: str=Form(...)):
    return f'YAY {taskname}'

@app.post("/prediction")
async def getPred(request: Request, prompt: str = Form(...)):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(103)
    res = generator(prompt, max_length=30, num_return_sequences=1)
    return res[0]["generated_text"]


@app.get("/items{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/health", status_code=200)
def health_check():
    return {"Everything": "OK!"}

