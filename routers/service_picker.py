from fastapi import APIRouter, Request, Form, status
from starlette.responses import RedirectResponse

from config import templates
from config import external_url
from atlas_service_client.service_client_factory import atlas_service_client
from service_client.service_registry_factory.registry_client_factory import registry_client
from fastapi.responses import JSONResponse
from atlas_service_client.db.db_context import DBContext
from atlas_service_client.db.db_client import db_client
from service_client.db.persistence_clients.service_client_persistence import AbstractServiceClientPersistence
from atlas_service_client.db.persistence_clients.user_persistence import AbstractUserPersistence

from pydantic import BaseModel
from config import app

service_picker_router = APIRouter()


class OAuthCodeFlowParams(BaseModel):
    code: str
    state: str


@service_picker_router.get('/service_picker')
def show_service_picker(request: Request):
    services = {}
    return templates.TemplateResponse('service_picker/service_picker.html', {"request": request,
                                                                             "service_info": services,
                                                                             "template_ids": get_template_ids(),
                                                                             "nav_items":
                                                                                 [['hello World > ',
                                                                                   app.url_path_for("show_hello_world")]
                                                                                  ],
                                                                             "username": request.cookies.get(
                                                                                 'username')})


@service_picker_router.post('/service_picker')
def show_service_picker(request: Request, template_selector: str = Form(...)):
    services = get_services_for_template_ids(template_selector)
    return templates.TemplateResponse('service_picker/service_picker.html', {"request": request,
                                                                             "service_info": services,
                                                                             "template_ids": get_template_ids(),
                                                                             "nav_items":
                                                                                 [['hello World > ',
                                                                                   app.url_path_for("show_hello_world")]
                                                                                  ],
                                                                             "username": request.cookies.get(
                                                                                 'username')})


@service_picker_router.post('/pair_selected_service')
def pair_selected_service(request: Request, service_id: str = Form(...)):
    service_client = atlas_service_client(service_id,
                                          external_url + app.url_path_for('finalize_oauth2_authorization_code_flow'))
    service_client.pair_service()
    redirect_url = service_client.trigger_oauth2_authorization_code_flow()
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    response.set_cookie('service_id', service_id)
    return response


@service_picker_router.get('/oauth2_code_flow')
def finalize_oauth2_authorization_code_flow(request: Request, code: str, state: str):
    print('finalizing authorization code flow')

    service_client_persistence: AbstractServiceClientPersistence = db_client(DBContext.Service_Client)
    grant_code_flow_state = service_client_persistence.get_oauth2_code_flow_state(state)

    user_persistence: AbstractUserPersistence = db_client(DBContext.User_Management)
    db_user = user_persistence.fetch_user(request.cookies.get('username'))

    user_id = db_user.user_id
    service_id = grant_code_flow_state.service_id
    service_name = grant_code_flow_state.service_name
    oauth2_auth_url = grant_code_flow_state.oauth2_auth_url
    oauth2_token_url = grant_code_flow_state.oauth2_token_url
    client_credentials = service_client_persistence.get_service_registration_data_by_auth_url(
        oauth2_auth_url)

    service_client = atlas_service_client(service_id,
                                          external_url + app.url_path_for('finalize_oauth2_authorization_code_flow'))

    service_client.finalize_oauth2_authorization_code_flow(code=code,
                                                           state=state,
                                                           service_registration_id=
                                                           client_credentials.registration_id,
                                                           oauth2_token_url=oauth2_token_url,
                                                           user_id=user_id,
                                                           service_name=service_name)
    return templates.TemplateResponse('service_picker/service_picker.html', {"request": request,
                                                                             "service_info": {},
                                                                             "template_ids": get_template_ids(),
                                                                             "nav_items":
                                                                                 [['hello World > ',
                                                                                   app.url_path_for("show_hello_world")]
                                                                                  ],
                                                                             "username": request.cookies.get(
                                                                                 'username')})


def get_services_for_template_ids(template_id):
    service_registry_client = registry_client()
    service_registry_client.request_access_token()
    services = {}
    services[template_id] = service_registry_client.get_services_implementing_template(template_id)
    return services


def get_template_ids():
    return ['sensor_data']
