from fastapi import APIRouter, Request
from config import templates, external_url
from atlas_service_client.service_client_factory import atlas_service_client
from atlas_service_client.hello_world_service_client import AbstractHelloWorldServiceClient
from config import app
from atlas_service_client.db.db_client import db_client
from atlas_service_client.db.db_context import DBContext
from service_client.db.persistence_clients.service_client_persistence import AbstractServiceClientPersistence
from atlas_service_client.db.persistence_clients.user_persistence import AbstractUserPersistence
from routers.service_picker import get_template_ids

hello_world_router = APIRouter()


@hello_world_router.get('/hello_world')
def show_hello_world(request: Request):
    data = {}
    service_id = request.cookies.get('service_id')
    user_persistence: AbstractUserPersistence = db_client(DBContext.User_Management)
    db_user = user_persistence.fetch_user(request.cookies.get('username'))

    service_client_persistence: AbstractServiceClientPersistence = db_client(DBContext.Service_Client)
    user_service_data = service_client_persistence.get_user_services_by_user_and_services_id(db_user.user_id,
                                                                                             service_id)

    if user_service_data is None:
        services = {}
        return templates.TemplateResponse('service_picker/service_picker.html', {"request": request,
                                                                                 "service_info": services,
                                                                                 "template_ids": get_template_ids(),
                                                                                 "nav_items":
                                                                                     [['hello World > ',
                                                                                       app.url_path_for(
                                                                                           "show_hello_world")]
                                                                                      ],
                                                                                 "username": request.cookies.get(
                                                                                     'username')})
    else:
        service_client: AbstractHelloWorldServiceClient = atlas_service_client(service_id,
                                                                               external_url + app.url_path_for(
                                                                                   'finalize_oauth2_authorization_code_flow'))

        data = service_client.get_data(user_service_data.service_id, user_service_data.user_token_id)
        print(data)
        return templates.TemplateResponse('hello_world/hello_world.html', {"request": request, "data": data, "username": request.cookies.get(
                                                                                     'username')})
