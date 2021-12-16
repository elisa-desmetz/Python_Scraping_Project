
from selenium import webdriver
from fastapi import FastAPI, HTTPException

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import logging

app = FastAPI()

@app.get("/")
def root():
    logging.info("a")
    return "Service is running..."