import logging
from pydantic import BaseModel, BaseSettings, AnyUrl, Json
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import os
from fastapi import FastAPI, Depends
from routers.service_picker import service_picker_router
from routers.hello_world import hello_world_router
from routers.user import user_router
from config import app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print(Path(__file__).parent.absolute() / "static")

prefix = os.getenv("PREFIX_URI", "/hello_world")

app.include_router(hello_world_router, prefix=prefix)
app.include_router(service_picker_router, prefix=prefix)
app.include_router(user_router, prefix=prefix)

app.mount(prefix + "/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")

origins = [
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
