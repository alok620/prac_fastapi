from typing import List, Dict, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

from transformers import pipeline, set_seed
import base64

from fastapi import FastAPI, status, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .imps import imp

from .d_mini import d_mini

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


@app.post("/prediction")
async def getPred(pred: Prediction):
    prompt = pred.instances[0]['prompt']
    d_mini.generate_image(
  	is_mega=False,
  	text=prompt,
  	seed=-1,
  	grid_size=1,
  	top_k=256,
  	image_path='generated',
  	models_root='pretrained',
     	fp16=False,
    ) 
    
    with open('/static/images/generated.png', mode='rb') as file:
        img = file.read()
    img = base64.encodebytes(img).decode('utf-8')
    return {"predictions": img}

@app.post("/submit")
async def getPred(request: Request, prompt: str = Form(...)):
    d_mini.generate_image(
            is_mega=False,
            text=prompt,
            seed=-1,
            grid_size=2,
            top_k=256,
            image_path='generated',
            models_root='pretrained',
            fp16=False,
        )


@app.get("/items{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/health", status_code=200)
def health_check():
    return {"Everything": "OK!"}

