from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
import os

app = FastAPI()
templates: Jinja2Templates = Jinja2Templates(directory="templates")
external_url = os.getenv("REDIRECT_URL", "http://10.0.75.2:8083")
prefix = os.getenv("PREFIX_URI", "/analysis-service")