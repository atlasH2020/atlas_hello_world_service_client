from fastapi import APIRouter, Request, Form, Response
from config import app, templates, external_url, prefix
from user_management.user_manager import user_manager_factory
from pydantic import BaseModel, BaseSettings, AnyUrl
from starlette.responses import RedirectResponse

from fastapi import Security, HTTPException, status
from pydantic import Json
import hashlib
from urllib.parse import urlencode
import requests
import json
import os


class SessionData(BaseModel):
    username: str


test_user = SessionData(username='')

user_router = APIRouter()


@user_router.route('/logout')
def logout(request: Request):
    request.cookies.pop('username')
    request.cookies.pop('service_id')
    login_url = external_url + prefix + '/login'
    response = RedirectResponse(url=login_url, status_code=status.HTTP_302_FOUND)
    return response


@user_router.get('/')
def root(request: Request):
    return RedirectResponse(url=app.url_path_for("login_user"), status_code=status.HTTP_302_FOUND)


@user_router.get('/register')
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@user_router.post('/register')
def register_page(request: Request, username: str = Form(...), password: str = Form(...)):
    user_manager_client = user_manager_factory()
    user_manager_client.register_user(username, password)
    return templates.TemplateResponse("landing_page.html", {"request": request})


@user_router.get('/login')
def login_user(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})


@user_router.get('/service_picker')
def show_portal(request: Request):
    baseURL = external_url + prefix + ''
    response = templates.TemplateResponse("/service_picker/service_picker.html",
                                          {"request": request, "username": request.cookies.get('username')})
    response.set_cookie(key='baseURL', value=baseURL)
    return response


@user_router.post('/login')
def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    user_manager_client = user_manager_factory()
    login_exists = user_manager_client.login_user(username, password)

    if login_exists:
        test_user = SessionData(username=username)
        services = {}
        redirect_url = external_url + prefix + '/service_picker'
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.set_cookie(key='username', value=test_user.username)
        return response
    else:
        return templates.TemplateResponse("landing_page.html", {"request": request})
