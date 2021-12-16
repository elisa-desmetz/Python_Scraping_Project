
from selenium import webdriver
from fastapi import FastAPI, HTTPException

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import static.functions as fun

from pyvirtualdisplay import Display

import logging
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

dfs = []

@app.get("/")
def root(request:Request):
    logging.info("a")
    display = Display(visible=0, size=(1027,768))
    display.start()

    dfs =  fun.export_dataframes()

    display.stop()
    logging.info("a")
    return templates.TemplateResponse(
        'df_representation.html',
        {'request': request, 'data': dfs[0].to_html()}
    )