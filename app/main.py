from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import static.functions as fun

import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

dfs = []

@app.get("/")
def root(request:Request):
    return templates.TemplateResponse(
        'index.html',
        {'request': request}
    )

@app.get("/table/{index:int}")
def table(request:Request, index=None):
    """
    Display the page called.
    """
    index = index
    ladder =  fun.export_dataframe(fun.categories[index])
    
    if index >3:
        return RedirectResponse(url="/") 
    
    return templates.TemplateResponse(
        'df_representation.html',
        {'request': request, 'data': ladder['df'].to_html(), 'name':ladder['name']}
    )